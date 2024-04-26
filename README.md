# Job Application Helper

Job Application Helper is a Python-based application that assists job seekers in creating customized cover letters and CV summaries tailored to specific job requirements. The application utilizes various language models and libraries to extract key information from job ads, candidate CVs, and sample cover letters to generate personalized application materials.

## Features

- Extract job requirements from a given job ad URL or pasted content
- Summarize candidate's CV to highlight relevant skills and education
- Generate customized cover letters based on job requirements, candidate's CV, and additional observations
- Support for multiple language models, including Claude3 Opus, GPT-3.5 Turbo, and GPT-4
- User-friendly web interface built with Streamlit

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/job-application-helper.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the necessary environment variables in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
IS_LOCAL=true
```

4. Run the application:

```bash
streamlit run src/app.py
```

## Usage

1. Open the application in your web browser.
2. Select the desired language model from the dropdown menu.
3. Provide the job ad URL or paste the job ad content into the text area.
4. The application will extract the job requirements and display them.
5. Review the generated CV summary, which highlights the candidate's relevant skills and education.
6. Add any additional instructions or observations in the provided text area.
7. Click the "Generate Cover Letter" button to create a customized cover letter.
8. Review the generated cover letter and make any necessary adjustments.

## Project Structure

```
├── .env
├── .env_example
├── LICENSE
├── input
│   ├── candidate_cv.pdf
│   └── cover_letter_sample.pdf
├── packages.txt
├── pyproject.toml
└── src
    ├── app.py
    ├── jobapplicationhelper
    │   └── __init__.py
    └── llms.py
```

- `.env`: File containing environment variables (not included in the repository)
- `.env_example`: Example file showing the structure of the `.env` file
- `LICENSE`: License file for the project
- `input/`: Directory containing input files (candidate CV and sample cover letter)
- `packages.txt`: List of required system packages
- `pyproject.toml`: Configuration file for the project dependencies
- `src/app.py`: Main application file
- `src/jobapplicationhelper/`: Package directory for the application
- `src/llms.py`: File containing the language model configuration and selection

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Langchain](https://github.com/hwchase17/langchain) - Building applications with LLMs through composability
- [Streamlit](https://streamlit.io/) - The fastest way to build and share data apps
- [OpenAI](https://openai.com/) - AI research and deployment company
- [Anthropic](https://www.anthropic.com/) - AI research company
