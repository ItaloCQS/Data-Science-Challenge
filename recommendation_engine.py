def get_recommendations(campaign_row, dataframe):
    
    recommendations = []

    excellent_campaign = campaign_row["klike_score"] >= 90

    if excellent_campaign:
        recommendations.append({
            "prioridade": "Info",
            "impacto_estimado": 999.0,
            "metrica": "Benchmark",
            "texto": (
                "Sua campanha já está com performance excelente. "
                "Recomendamos priorizar testes A/B incrementais; "
                "as sugestões abaixo representam apenas otimizações marginais."
            )
        })

    # Benchmarks
    avg_ctr_with_hook = dataframe[dataframe["has_hook"] == True]["ctr"].mean()
    avg_ctr_no_hook = dataframe[dataframe["has_hook"] == False]["ctr"].mean()

    avg_conv_with_cta = dataframe[dataframe["has_cta"] == True]["conversions"].mean()
    avg_conv_no_cta = dataframe[dataframe["has_cta"] == False]["conversions"].mean()

    avg_watch_face = dataframe[dataframe["has_face"] == True]["avg_watch_time_s"].mean()
    avg_watch_no_face = dataframe[dataframe["has_face"] == False]["avg_watch_time_s"].mean()

    uplift_hook = (
        ((avg_ctr_with_hook / avg_ctr_no_hook) - 1) * 100
        if avg_ctr_no_hook > 0 else 0
    )

    uplift_cta = (
        ((avg_conv_with_cta / avg_conv_no_cta) - 1) * 100
        if avg_conv_no_cta > 0 else 0
    )

    uplift_face = (
        ((avg_watch_face / avg_watch_no_face) - 1) * 100
        if avg_watch_no_face > 0 else 0
    )

    # Regras principais
    if not campaign_row["has_hook"]:
        recommendations.append({
            "prioridade": "Alta",
            "impacto_estimado": uplift_hook,
            "metrica": "CTR",
            "texto": (
                f"Adicionar um hook nos primeiros 3s pode elevar o CTR "
                f"em aproximadamente {uplift_hook:.1f}% com base nos padrões do dataset."
            )
        })

    if not campaign_row["has_cta"]:
        recommendations.append({
            "prioridade": "Alta",
            "impacto_estimado": uplift_cta,
            "metrica": "Conversões",
            "texto": (
                f"Incluir um CTA explícito pode aumentar as conversões "
                f"em cerca de {uplift_cta:.1f}%."
            )
        })

    if not campaign_row["has_face"]:
        recommendations.append({
            "prioridade": "Média",
            "impacto_estimado": uplift_face,
            "metrica": "Retenção",
            "texto": (
                f"Incluir rosto humano no criativo pode elevar o tempo médio "
                f"assistido em aproximadamente {uplift_face:.1f}%."
            )
        })

    # Regras contextuais
    platform = campaign_row["platform"]
    duration = campaign_row["video_duration_s"]
    video_format = campaign_row["format"]

    # TikTok
    if platform == "TikTok":
        if video_format != "vertical":
            recommendations.append({
                "prioridade": "Alta",
                "impacto_estimado": 18.0,
                "metrica": "ROAS",
                "texto": (
                    "No TikTok, migrar para formato vertical pode melhorar "
                    "retenção e ROAS em aproximadamente 18%."
                )
            })

        if duration > 25:
            recommendations.append({
                "prioridade": "Média",
                "impacto_estimado": 15.0,
                "metrica": "Retenção",
                "texto": (
                    "No TikTok, reduzir a duração para 15–20s pode melhorar "
                    "retenção e engajamento em torno de 15%."
                )
            })

    # LinkedIn
    elif platform == "LinkedIn":
        if video_format != "horizontal":
            recommendations.append({
                "prioridade": "Média",
                "impacto_estimado": 12.0,
                "metrica": "Watch Time",
                "texto": (
                    "No LinkedIn, migrar para formato horizontal pode elevar "
                    "o watch time em aproximadamente 12%, melhorando retenção "
                    "e percepção de qualidade."
                )
            })

        if duration < 20:
            recommendations.append({
                "prioridade": "Baixa",
                "impacto_estimado": 8.0,
                "metrica": "Retenção",
                "texto": (
                    "Criativos no LinkedIn performam melhor com narrativas mais longas. "
                    "Expandir para 30–45s pode aumentar retenção em cerca de 8%."
                )
            })

    # Meta
    elif platform == "Meta":
        if video_format not in ["vertical", "quadrado"]:
            recommendations.append({
                "prioridade": "Média",
                "impacto_estimado": 10.0,
                "metrica": "Engagement",
                "texto": (
                    "No Meta, migrar para formato vertical ou quadrado pode "
                    "elevar o engajamento em aproximadamente 10%, especialmente "
                    "em Reels e Feed."
                )
            })

    fallback_recommendations = [
        {
            "prioridade": "Baixa",
            "impacto_estimado": 7.0,
            "metrica": "Klike Score",
            "texto": (
                "Testar variações de abertura e ritmo narrativo pode elevar "
                "o Klike Score em aproximadamente 7 pontos."
            )
        },
        {
            "prioridade": "Baixa",
            "impacto_estimado": 6.0,
            "metrica": "Retenção",
            "texto": (
                "Ajustar a densidade de texto para nível médio pode melhorar "
                "retenção em cerca de 6%."
            )
        },
        {
            "prioridade": "Baixa",
            "impacto_estimado": 5.0,
            "metrica": "Engagement",
            "texto": (
                "Otimizar o equilíbrio entre música e voz pode aumentar "
                "engajamento em aproximadamente 5%."
            )
        }
    ]   

    i = 0
    while len(recommendations) < 3 and i < len(fallback_recommendations):
        recommendations.append(fallback_recommendations[i])
        i += 1

    recommendations = sorted(
        recommendations,
        key=lambda x: x["impacto_estimado"],
        reverse=True
    )

    return recommendations[:3]