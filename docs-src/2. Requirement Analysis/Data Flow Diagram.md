# Data Flow Diagram

{{HEADER:2 Marks}}

## Level 0 - Context Diagram

```
 ( Student / Browser )                                       ( Google Gemini API )
        |   ^                                                      ^    |
        |   | answer, summary, quiz,                  prompt       |    | generated text
        |   | learning path, error message                         |    v
        v   |                                                      |
   +--------------------------------------------------------------------------+
   |                          EduGenie  (FastAPI)                              |
   +--------------------------------------------------------------------------+
                                  |
                       (no database: nothing is stored)
```

## Level 1 - Main Processes

```
 ( Student )
   | 1 task + text (+ previous answer for follow-ups)
   v
 +--------------------+   invalid input   +--------------------------+
 | 1.0 Validate Input |------------------>| error message to student |
 | (empty? too long?) |                   +--------------------------+
 +---------+----------+
           | valid text
           v
 +--------------------+
 | 2.0 Build Prompt   |  qna / explanation / summary / quiz / learning path module
 +---------+----------+
           | prompt
           v
 +--------------------+  prompt   ( Gemini API )
 | 3.0 Call Gemini    |---------->
 | (API key from .env,|<----------  generated text
 |  model fallback)   |
 +---------+----------+
           | raw text
           v
 +--------------------+
 | 4.0 Format Result  |  quiz: remove code fences, parse JSON, validate 3 x 4 options
 +---------+----------+
           | result
           v
      ( Student )
```

| Symbol | Name | Meaning in this project |
|---|---|---|
| Oval ( ) | External entity | Student (browser), Google Gemini API |
| Numbered box | Process | 1.0 Validate Input, 2.0 Build Prompt, 3.0 Call Gemini, 4.0 Format Result |
| [ ] | Data store | None. EduGenie keeps no database; the browser holds the last answer in memory only, for follow-up questions |
| Arrow | Data flow | Labeled on the diagram |
