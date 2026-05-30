# Writing the description (the part that makes a skill trigger)

The `description` is the only text loaded at startup. The model picks skills from it.
A weak description means a great skill never fires. Treat it as the highest-leverage
sentence in the whole file.

## Rules

1. **Third person.** "Extracts text from PDFs…", not "I can…" or "You can…". First/second person degrades discovery.
2. **What AND when.** State the capability and the trigger. The "when" is what the model matches against.
3. **Lead with the use case.** The model may only see the first ~1500 chars across all skills; front-load the trigger terms.
4. **Concrete trigger terms.** Use the words a user would actually say.
5. **<= 1024 chars.** One or two sentences.

## Good

```
description: Extracts text and tables from PDFs, fills forms, merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
```
description: Analyzes Excel spreadsheets, builds pivot tables, generates charts. Use when analyzing .xlsx files, spreadsheets, or tabular data.
```
```
description: Conversion copywriter. Writes landing-page copy and email sequences, and rewrites AI-sounding drafts to read human. Use when writing or editing marketing copy, headlines, value props, or onboarding emails.
```

## Bad

```
description: Helps with documents          # vague, no trigger
description: The Editor. Manages clarity.  # persona label, no "when"
description: I can help you write copy     # first person
```

## Examples beat instructions

If output quality depends on a specific style, the strongest lever is not more rules,
it is input/output pairs in the body. Show two or three examples of the exact shape
you want. One good example outperforms a paragraph of description.