def format_prompt(user_input, klaviyo_data):
    email_metrics = klaviyo_data.get("data", [])
    summary = f"User input: {user_input}\n\nRecent Klaviyo Metrics:\n"

    for item in email_metrics[:5]:  # Limit to first 5 items for brevity
        summary += f"- {item.get('attributes', {}).get('name', 'N/A')}\n"

    return (
        f"You are a marketing strategist. Using the following Klaviyo data, "
        f"write a performance-oriented, elegant email campaign suggestion:\n\n{summary}"
    )
