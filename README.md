# JobApplicationHelper

JobApplicationHelper is a Python project that helps job applicants create customized CV summaries and cover letters based on the requirements of a specific job position. The project utilizes various libraries and APIs to extract job requirements from a given URL, generate tailored content, and provide an interactive user interface.

## Project Structure

The project has the following structure:

```
JobApplicationHelper/
  .env
  README.md
  poetry.lock
  pyproject.toml
  input/
    candidate_cv.txt
    cover_letter_sample.txt
  src/
    app.py
    llms.py
```

- `.env`: Contains environment variables for API keys (OpenAI and Anthropic).
- `README.md`: This file, providing an overview of the project.
- `poetry.lock` and `pyproject.toml`: Configuration files for the Poetry dependency management tool.
- `input/`: Directory containing input files.
  - `candidate_cv.txt`: The candidate's CV content.
  - `cover_letter_sample.txt`: A sample cover letter.
- `src/`: Directory containing the project's source code.
  - `app.py`: The main application file.
  - `llms.py`: Module for handling language models and APIs.

## Dependencies

The project relies on the following dependencies:

- Python (version 3.10 to 3.13)
- python-dotenv
- setuptools
- decouple
- openai
- langchain
- langchain-community
- langchain-anthropic
- playwright
- html2text
- beautifulsoup4
- streamlit
- langchain-openai

These dependencies are managed using the Poetry dependency management tool. The specific versions are specified in the `pyproject.toml` file.

## Usage

1. Set up the required API keys in the `.env` file:
   ```
   OPENAI_API_KEY=''
   ANTHROPIC_API_KEY=''
   ```

2. Install the project dependencies using Poetry:
   ```
   poetry install
   ```

3. Run the application:
   ```
   poetry run streamlit run src/app.py
   ```

4. Access the application through the provided URL in your web browser.

5. Paste the URL of the job position you are interested in into the text input field.

6. The application will extract the job requirements from the provided URL, generate a customized CV summary and cover letter based on the candidate's CV and the sample cover letter.

7. The generated content will be displayed on the screen, along with the extracted job requirements and the history of the CV summary and cover letter generation.

## Customization

- You can modify the input files (`candidate_cv.txt` and `cover_letter_sample.txt`) to provide your own CV content and cover letter sample.

- The prompt templates used for generating the CV summary and cover letter can be customized in the `app.py` file.

- Additional language models and APIs can be added or modified in the `llms.py` file.

## License

This project is open-source and available under the [MIT License](LICENSE).