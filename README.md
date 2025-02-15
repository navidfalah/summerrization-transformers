# 🐍 Summarization with Transformers

## 📝 Description
This Python script demonstrates how to perform **text summarization** using transformer models like **Pegasus**, **BART**, **T5**, and **GPT-2**. It evaluates these models on the **CNN/DailyMail** and **SAMSum** datasets using metrics like **ROUGE** and **BLEU**. The script also includes a baseline summarization method and fine-tuning capabilities for the Pegasus model. 🛠️

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/navidfalah/summarization-transformers.git
   cd summarization-transformers
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install additional libraries:
   ```bash
   pip install datasets evaluate sacrebleu rouge_score
   ```

---

## 🚀 Usage

1. Run the script:
   ```bash
   python summarization_transformers.py
   ```

2. The script will:
   - Load the CNN/DailyMail and SAMSum datasets.
   - Generate summaries using baseline methods and pre-trained models (Pegasus, BART, T5, GPT-2).
   - Evaluate summaries using ROUGE and BLEU metrics.
   - Fine-tune the Pegasus model on the SAMSum dataset.
   - Visualize token length distributions for dialogues and summaries.

---

## 📂 File Structure

```
summarization-transformers/
├── summarization_transformers.py  # Main script
├── README.md                      # This file
├── requirements.txt               # Dependencies
└── data/                          # (Optional) Data folder for local datasets
```

---

## 🧩 Key Features

- **Text Summarization**:
  - Use pre-trained models like Pegasus, BART, T5, and GPT-2 for summarization.
  - Fine-tune Pegasus on the SAMSum dataset for dialogue summarization.

- **Evaluation**:
  - Evaluate summaries using ROUGE and BLEU metrics.
  - Compare model performance with a baseline method.

- **Visualization**:
  - Plot token length distributions for dialogues and summaries.

- **Custom Summarization**:
  - Generate summaries for custom text inputs.

---

## 📊 Example Outputs

1. **Summarization Example**:
   - Input: "The U.S. are a country. The U.N. is an organization."
   - Output: "The U.S. are a country. The U.N. is an organization."

2. **ROUGE Scores**:
   - ROUGE-1: 0.45
   - ROUGE-2: 0.30
   - ROUGE-L: 0.40

3. **BLEU Score**:
   - BLEU: 0.25

---

## 🤖 Models Used

- **Pegasus**: A pre-trained transformer model fine-tuned for summarization tasks.
- **BART**: A sequence-to-sequence model for text generation and summarization.
- **T5**: A text-to-text transformer model.
- **GPT-2**: A generative pre-trained transformer model.

---

## 📈 Performance Metrics

- **ROUGE Scores**:
  - ROUGE-1, ROUGE-2, and ROUGE-L metrics for evaluating summarization quality.

- **BLEU Score**:
  - BLEU metric for evaluating the precision of generated summaries.

---

## 🛠️ Dependencies

- Python 3.x
- Libraries:
  - `transformers`, `datasets`, `evaluate`
  - `torch`, `matplotlib`, `pandas`
  - `sacrebleu`, `rouge_score`

---

## 🤝 Contributing

Contributions are welcome! 🎉 Feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Hugging Face for the `transformers` library.
- The CNN/DailyMail and SAMSum datasets for providing summarization data.
- Google Research for the Pegasus model.

---

## 👤 Author

- **Name**: Navid Falah
- **GitHub**: [navidfalah](https://github.com/navidfalah)
- **Email**: navid.falah7@gmail.com
