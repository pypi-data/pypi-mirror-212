def catalogue_yaml() -> str:
    return """
        test_table:
          datetime_column: created_at
          columns:
          - name: name
            deidentifier:
              type: redact
            period: P365D # [±]P[DD]DT[HH]H[MM]M[SS]S
            description: Name of user
          - name: email
            deidentifier:
              type: replace
              value: fake@email.com
            period: P365D # [±]P[DD]DT[HH]H[MM]M[SS]S
          - name: ip
            deidentifier:
              type: mask
              value: "#"
            period: "280 00" # [-][DD ][HH:MM]SS[.ffffff]
    """
