# Weird listings

````markdown
This listing contains a **Markdown** listing:

```markdown
inner *listing*
```
````

Empty listing, no language:
```
```

Empty listing, python:
```python
```

Mermaid diagrams from <https://squidfunk.github.io/mkdocs-material/reference/diagrams/>:
``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```

``` mermaid
sequenceDiagram
  autonumber
  Alice->>John: Hello John, how are you?
  loop Healthcheck
      John->>John: Fight against hypochondria
  end
  Note right of John: Rational thoughts!
  John-->>Alice: Great!
  John->>Bob: How about you?
  Bob-->>John: Jolly good!
```
