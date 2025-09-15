# Tone of Voice Guidelines

## About this document

These content guidelines are intended to support the RBSI Onboarding Delivery. Our aim is to keep messaging, labels, questions and comms consistent in terms of tone of voice and usage. It's a living document, and is based on guidelines provided by NatWest, combined with best practice for effective UX.

---

*Nile HQ Ltd is registered in Scotland no. SC306908*  
*Registered office: 13-15 Circus Lane, Edinburgh, EH3 6SU, UK*

---

## We put customers first

### Tone of voice

We believe forms should feel like a conversation between two people, not a bank and a customer. This means we talk like a person, not like a bank. Our goal is to use language that's simple, everyday, and easy to read.

We always write from the customer's perspective. It's not about what we want to ask; it's about what the customer needs to know to move forward.

#### Key principles

**Keep it human.** We're here to help, so our copy should feel chatty, not formal. Be honest and human in your phrasing.

**Simple is smart.** The average reading age in the UK is 9 years old, so we should write for that level. Use simple words and avoid banking jargon. For example, use "get in touch" instead of "contact us."

**Be direct.** Put the most important words first and cut anything unnecessary. If you're writing help text, there's no need to say "This is the total cost"—just say "Total cost."

**Build empathy.** Step into our users' shoes. Ask yourself: What are we inspiring them to do? What do they need to know? What's getting in the way?

**User-focused phrasing.** Make sure your language addresses the user directly. Use "you" and "your" when the service is speaking (e.g., "your business"), and "I," "me," or "my" when the user is hypothetically speaking.

**Keep copy short and direct.** Break up copy into short sentences. One idea per sentence.

### Pronouns (we, you, me, my)

Forms are like a conversation between the service and the user.

If it's the service 'speaking', the user is 'you' or 'your' and the service is 'we', 'us', 'our' and so on.

If it's the user 'speaking', use 'I', 'me' or 'my'.

This applies to all microcopy, including headings, input labels and link text.

### Structure

Break up long pages with headings. It's easier to scan and read. Headings should describe the purpose of the text that follows - they shouldn't be part of the text.

Screen reader users often read out lists of links in isolation, so make the purpose of the link clear from the link text alone. For example, 'click here' is not accessible link text.

### Ask smart questions

Only ask a question if you know:
- that you need the information to deliver the service
- why you need the information
- what you'll do with it
- which users need to give you the information
- how you'll check the information is accurate
- how to keep the information secure

### Add help text where necessary

Sometimes it's useful to provide help text to explain things like:
- legal jargon
- where to find obscure information
- what format the information should be given in
- what you'll do with a user's personal information
- the consequences of making one choice over another

Only add help text if you see in research that users need it.

---

## Automated Tone Analysis

### Running the Analysis

We have an automated tool to check question sets against these guidelines:

```bash
python3 scripts/analyze_tone.py \
  --schema apps/prototype/data/schemas/your-journey/schema.yaml \
  --output tone_analysis.csv \
  --summary
```

### What it checks

The analyzer reviews each question for:
- **Length** - Flags questions over 20 words
- **Jargon** - Identifies banking/legal terms
- **Passive voice** - Suggests active alternatives
- **Pronouns** - Checks for "you/your" vs "the entity"
- **Complexity** - Identifies multi-clause sentences

### Review Process

1. **Run the analysis** - Generates CSV report
2. **Review suggestions** - Open CSV in spreadsheet
3. **Make decisions** - Accept/Reject/Modify each suggestion
4. **Document rationale** - Add notes for audit trail
5. **Apply changes** - Update source or schema

### CSV Report Format

| Column | Description |
|--------|-------------|
| row_ref | Source spreadsheet reference |
| field_key | Field identifier |
| issue_type | Type of tone issue |
| severity | High/Medium/Low |
| details | Specific details |
| original | Original question text |
| suggestion | Recommended rewrite |
| human_decision | Your decision (Accept/Reject/Modified) |
| notes | Rationale for decision |

### Integration with Import

You can run tone analysis during import:

```bash
# First import the data
python3 scripts/import_xlsx_kycp.py [options]

# Then analyze tone
python3 scripts/analyze_tone.py \
  --schema apps/prototype/data/schemas/journey-kycp/schema-kycp.yaml \
  --output analysis/journey_tone_analysis.csv
```

### Best Practice

- Run analysis on every new import
- Keep CSV reports for audit trail
- Track improvement over time
- Share reports with content team
- Update source spreadsheets based on accepted changes

---

*Nile HQ Ltd is registered in Scotland no. SC306908*  
*Registered office: 13-15 Circus Lane, Edinburgh, EH3 6SU, UK*