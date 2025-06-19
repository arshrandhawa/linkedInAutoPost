<table align="center">
  <tr>
	<td align="center">
      <a href="https://github.com/arshrandhawa/portfolio/blob/main/README.md">
        <img src="https://img.shields.io/badge/-Homepage-gray?style=for-the-badge&logo=github&scale=2" alt="Homepage">
      </a>
    </td>
	<td align="center">
      <a href="https://github.com/arshrandhawa/BusinessIntelligencePortfolio/blob/main/README.md">
        <img src="https://img.shields.io/badge/-Business_Intelligence-blue?style=for-the-badge&logo=tableau&scale=4" alt="Business Intelligence">
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/arshrandhawa/DataAnalystPortfolio/blob/main/README.md">
        <img src="https://img.shields.io/badge/-Data_Analyst-green?style=for-the-badge&logo=sqlite&scale=4" alt="Data Analyst">
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/arshrandhawa/DataEngineerPortfolio/blob/main/README.md">
        <img src="https://img.shields.io/badge/-Data_Engineering-orange?style=for-the-badge&logo=docker&scale=4" alt="Data Engineering">
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/arshrandhawa/DataScientistPortfolio/blob/main/README.md">
        <img src="https://img.shields.io/badge/-Data_Science-purple?style=for-the-badge&logo=scikit-learn&scale=4" alt="Data Science">
      </a>
    </td>
  </tr>
</table>

# LinkedIn Auto Post

### Automating LinkedIn Engagement

This project automates the process of posting engaging content on LinkedIn, ensuring consistent presence and enhanced networking. It is designed to schedule and publish posts on a weekly or biweekly basis without requiring manual intervention.

## Features

- ✅ **Automated Posting**: Automatically schedules and posts content to LinkedIn via GitHub Workflows.
- ✅ **JSON-Based Content Storage**: Post content is stored in a structured JSON file for easy updates and flexibility.
- ✅ **Logging & Error Handling**: Tracks post success and errors in a log file to facilitate debugging.
- ✅ **Secure Credentials Management**: Authentication details are securely stored in GitHub Secrets, with a reminder to update them every two months.

## Project Structure

```
.github/workflows/        # GitHub Actions configuration for scheduling posts
data/                    # Directory containing JSON files with post content
logs/                    # Directory for log files (tracking post activities)
main.py                  # Python script for handling LinkedIn API requests
requirements.txt         # List of dependencies required for the project
README.md                # Documentation for the project
```

## Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/LinkedInAutoPost.git
cd LinkedInAutoPost
```

### 2. Install dependencies

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

### 3. Configure authentication

- Store your LinkedIn API credentials in GitHub Secrets. 
- Remember to update your credentials every two months for continued functionality.

### 4. Add new posts

- Edit the JSON file located in `/data/` to schedule and update posts.

### 5. Deploy & Schedule

- The workflow is defined in .github/workflows/ as a YAML file (actions.yml). It contains the instructions for when and how the script should run.

## Logging & Monitoring

- Log files are stored in the `/data/` directory.
- The log file will record both successful posts and errors. If a post fails, check the log for error details, and consider running a local debugging session.

## Future Enhancements

- 🔹 **AI-Generated Post Suggestions**: Automatically generate post ideas using AI algorithms.
- 🔹 **Engagement Analytics**: Implement analytics for tracking post performance and user engagement.

---

## 📬 Connect With Me

- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/arshrandhawa11/)
- **Tableau Public**: [My Tableau Public Profile](https://public.tableau.com/app/profile/arshdeep.randhawa6351/vizzes)
- **Email**: [arshdip.randhawa@gmail.com](mailto:arshdip.randhawa@gmail.com)

Thank you for visiting my portfolio! Feel free to reach out for collaborations or opportunities.
