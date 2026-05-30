---
name: deep-research
description: >-
  Deep research harness — fan-out web searches, fetch sources, adversarially
  verify claims, synthesize a cited report. Use when the user wants a deep,
  multi-source, fact-checked research report on any topic. BEFORE invoking,
  check if the question is specific enough to research directly — if
  underspecified (e.g., "what car to buy" without budget/use-case/region),
  ask 2-3 clarifying questions to narrow scope. Then pass the refined question
  as args, weaving the answers in.
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Bash
  - Agent
---

# Deep Research

A harness for producing a deep, multi-source, **fact-checked** research report
on a topic. The goal is a report whose every non-obvious claim is backed by a
citation to a source you actually fetched and read — not just searched.

## When to use

Use this when the user wants a thorough, cited answer that no single page can
provide: comparisons, "state of the art" surveys, due-diligence, market or
technical landscape questions, "should I X" decisions that hinge on facts.

Do **not** use it for quick lookups (a single search answers it) or for
questions about the local codebase (use normal code-search tools).

## Before you start: scope the question

If the question is underspecified, the report will be unfocused. Before
researching, check that you know enough to make the report useful. If not, ask
the user **2–3 sharp clarifying questions** covering the dimensions that would
most change the answer, e.g.:

- **Goal / decision**: what will they do with the answer?
- **Constraints**: budget, region, timeframe, scale, platform.
- **Depth & audience**: a quick brief vs. an exhaustive report; expert vs. lay.

Weave the answers into a single refined research question before continuing. If
the question is already specific, skip straight to planning.

## Workflow

### 1. Plan

Decompose the refined question into **3–6 sub-questions** that together cover
the topic. Write them down. Each sub-question should be independently
searchable and should map to a section of the final report.

### 2. Fan-out search

For each sub-question, run several **WebSearch** queries with varied phrasing
(synonyms, opposing framings, "X vs Y", "X limitations", "X criticism"). Cast a
wide net — aim for breadth of *distinct domains*, not just the top hits of one
query.

For large topics, dispatch sub-questions to parallel subagents (the `Agent`
tool, `Explore`/`general-purpose`) so searches run concurrently. Each subagent
returns candidate URLs + one-line relevance notes; you keep the synthesis.

### 3. Fetch and read sources

Searching is **not** reading. For every claim you intend to use, **WebFetch**
the actual page and read the relevant passage. Prefer primary sources (papers,
official docs, filings, standards, original reporting) over aggregators and
SEO content. Capture for each source: URL, title, publication date, author/
organisation, and the specific quote or figure that supports the claim.

### 4. Adversarially verify

This is the step that separates research from summarising. For each important
claim:

- **Corroborate**: find at least one *independent* source that agrees. Two
  outlets republishing the same wire story is one source, not two.
- **Seek disconfirmation**: actively search for evidence the claim is wrong,
  outdated, or contested. Search "<claim> debunked / criticism / wrong / update".
- **Check recency**: is the figure current as of today's date? Note "as of
  <date>" when values drift over time (prices, versions, leadership, law).
- **Trace provenance**: follow citations back to the origin. Distrust numbers
  with no traceable source.

Label each key claim as **Confirmed** (multiple independent sources),
**Single-source**, or **Contested**, and reflect that uncertainty in the report.

### 5. Synthesize the report

Write a structured, cited Markdown report:

- **TL;DR** — 3–6 bullet answer to the question up front.
- **Body** — one section per sub-question. Make claims, then cite. Use inline
  numbered citations `[1]`, `[2]` … that map to the Sources list.
- **Disagreements / open questions** — where sources conflict or evidence is
  thin, say so explicitly rather than papering over it.
- **Sources** — numbered list with title, publisher, date, and URL for every
  citation. Only list sources you actually fetched.

Hold a high bar: **every non-obvious factual claim must carry a citation** to a
source you read. If you could not verify something, say so instead of asserting
it. Distinguish established fact from your own inference or speculation.

## Output quality bar

- Cited, current, and honest about uncertainty.
- Breadth across independent sources, not one echoing cluster.
- Directly answers the user's *refined* question, at the requested depth.
- No fabricated sources, quotes, dates, or figures — ever.

## Anti-patterns

- Citing search-result snippets without fetching the page.
- Treating syndicated copies of one story as independent corroboration.
- Burying the answer — lead with the TL;DR.
- Presenting contested or single-source claims as settled fact.
- Padding length instead of adding verified substance.
