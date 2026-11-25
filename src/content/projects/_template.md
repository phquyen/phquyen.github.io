---
# HOW TO ADD A PROJECT
# 1. Copy this file in the same folder and rename it, e.g. sales-dashboard.md
#    (the file name becomes the page address: /projects/sales-dashboard/).
#    Use lowercase letters, numbers and dashes. Don't start it with "_".
# 2. Fill in the fields below and write the case study under the second ---.
# 3. Save, check it with `npm run dev`, then commit and push.
# Files starting with "_" (like this one) are ignored by the site.
# Full guide: EDITING.md in the main folder.

title: "Project title"
summary: "One or two sentences shown on the project card."
tools: ["Python", "SQL"]        # shown as tags; can be []
github: "https://github.com/phquyen/repo-name"   # optional: delete the line if none
demo: "https://example.com"     # optional: delete the line if none
featured: false                 # true = listed first, with a "Featured" label
order: 10                       # lower numbers appear first
draft: true                     # true = hidden on the live site (still shown in npm run dev)
---

## The problem

What question were you trying to answer, and for whom? Why did it matter?

## The data

Where did the data come from, and what made it messy?

## Approach

What did you do, step by step? Mention key decisions and trade-offs.

## Result

What did people learn or do differently because of it? Include numbers if you can.

## What I'd do next

Optional: what you would improve with more time.

<!-- Images: put them in the public/ folder and use ![Description](/my-image.png) -->
