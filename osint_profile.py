def summarize_osint_profile(osint_data):
    """
    Analyzes OSINT data and returns a digital profile summary with flagged patterns.
    """
    name = osint_data.get('name')
    username = osint_data.get('username')
    email = osint_data.get('email')
    phone = osint_data.get('phone')
    social_profiles = osint_data.get('social_profiles', {})
    breaches = osint_data.get('breaches', [])
    domains = osint_data.get('domains', [])

    summary_lines = []
    flags = []

    # Basic identity
    if name:
        summary_lines.append(f"The subject's name is {name}.")
    if email:
        summary_lines.append(f"Email address: {email}.")
    if phone:
        summary_lines.append(f"Phone number: {phone}.")
    if username:
        summary_lines.append(f"Known username: {username}.")

    # Social profiles
    if social_profiles:
        platforms = ', '.join(social_profiles.keys())
        summary_lines.append(f"Social profiles found on: {platforms}.")
        # Check for username reuse
        reused = [platform for platform, profile in social_profiles.items() if username and username in profile]
        if reused:
            flags.append(f"Username '{username}' reused on: {', '.join(reused)}.")
        # LinkedIn + phone + name
        if 'linkedin' in social_profiles and phone and name:
            flags.append(f"LinkedIn profile with phone number and name connection found.")

    # Email/username/phone cross-matches
    if email and username and username in email:
        flags.append(f"Username '{username}' appears in email address.")
    if phone and username and username in phone:
        flags.append(f"Username '{username}' appears in phone number.")

    # Breach data
    if breaches:
        summary_lines.append(f"Known breaches: {', '.join(breaches)}.")
        flags.append("Subject appears in known data breaches.")

    # Domain info
    if domains:
        summary_lines.append(f"Associated domains: {', '.join(domains)}.")

    # Interesting patterns
    if not flags:
        flags.append("No notable patterns detected.")

    # Compose summary
    summary = "Subject Profile\n"
    summary += " ".join(summary_lines) + "\n"
    summary += "Flagged Patterns: " + "; ".join(flags)
    return summary


def generate_osint_links(osint_data):
    """
    Given OSINT data, return a dict mapping each field to a list of clickable HTML links for investigation.
    Only name and username are used. Google dorking links are included for both.
    """
    name = osint_data.get('name')
    username = osint_data.get('username')
    links = {}

    if name:
        links['name'] = [
            f'<a href="https://www.google.com/search?q=\"{name}\"" target="_blank" title="Exact name search">Exact</a>',
            f'<a href="https://www.google.com/search?q=intitle:%22{name}%22" target="_blank" title="intitle dork">intitle</a>',
            f'<a href="https://www.google.com/search?q=intext:%22{name}%22" target="_blank" title="intext dork">intext</a>',
            f'<a href="https://www.google.com/search?q=site:linkedin.com+%22{name}%22" target="_blank" title="LinkedIn site dork">site:linkedin</a>',
            f'<a href="https://www.linkedin.com/search/results/people/?keywords={name}" target="_blank" title="Search LinkedIn">LinkedIn</a>'
        ]
    if username:
        links['username'] = [
            f'<a href="https://www.google.com/search?q=\"{username}\"" target="_blank" title="Exact username search">Exact</a>',
            f'<a href="https://www.google.com/search?q=inurl:%22{username}%22" target="_blank" title="inurl dork">inurl</a>',
            f'<a href="https://www.google.com/search?q=intitle:%22{username}%22" target="_blank" title="intitle dork">intitle</a>',
            f'<a href="https://www.google.com/search?q=intext:%22{username}%22" target="_blank" title="intext dork">intext</a>',
            f'<a href="https://www.google.com/search?q=site:github.com+%22{username}%22" target="_blank" title="GitHub site dork">site:github</a>',
            f'<a href="https://github.com/{username}" target="_blank" title="Check username on GitHub">GitHub</a>',
            f'<a href="https://twitter.com/{username}" target="_blank" title="Check username on Twitter">Twitter</a>',
            f'<a href="https://instagram.com/{username}" target="_blank" title="Check username on Instagram">Instagram</a>',
            f'<a href="https://namechk.com/{username}" target="_blank" title="Check username on Namechk">Namechk</a>'
        ]
    return links


if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) > 1 and sys.argv[1] == 'links':
        osint_data = json.load(sys.stdin)
        links = generate_osint_links(osint_data)
        print(json.dumps(links))
    else:
        osint_data = json.load(sys.stdin)
        print(summarize_osint_profile(osint_data))
