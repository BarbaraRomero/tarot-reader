# The Three-Card Oracle

A classroom tarot app. Students type a question, draw three random cards (Past · Present · Future), read each card's traditional meaning, and write their own interpretation. Then they can reveal an AI's interpretation and compare.

- 78 Rider–Waite–Smith cards, each drawn upright or reversed (30% chance of reversed)
- Card meanings from A. E. Waite, *The Pictorial Key to the Tarot* (1910), parsed into `cards.json`
- The AI interpretation is hidden until the student has written their own reading (15+ words)
- The AI runs entirely in the browser with [Transformers.js](https://huggingface.co/docs/transformers.js):
  - **Llama 3.2 1B Instruct** on computers with WebGPU (recent Chrome/Edge), about 1.2 GB, downloaded once
  - **Qwen 2.5 0.5B Instruct** as a fallback elsewhere (smaller, simpler readings)
- The AI writes a short paragraph per card plus a short final message, in English (about 6 seconds once loaded), and names the model that wrote it
- The model starts downloading as soon as the cards are drawn, while students write
- Questions should be asked in English

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Rebuilding the card meanings

`tools/parse_lwb.py` turns the text of the deck's booklet into `cards.json`. Only Waite's card meanings are used.

## Credits

By Bárbara Romero Ferrón, with the invaluable help of Claude.
Card art by Pamela Colman Smith (1909); card meanings by A. E. Waite (1910); both in the public domain.
