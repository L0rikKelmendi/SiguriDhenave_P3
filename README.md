🛸 🌎　°　　🌓　•　　.°•　🚀 ✯ 　　　★　*　　　　　°　🛰 　°·　　🪐 .　　　•　° ★　• ☄ 
▁▂▃▄▅▆▇▇▆▅▄▃▁▂▁▂▃▄▅▆▇▇▆▅▄▃▁▂

University of Prishtina " Hasan Prishtina '
Faculty of Electrical and Computer Engineering

Project Title: Two-Factor Authentication (2FA) System

**Contributors:**

_Brela_,

_Blerton_,

_Pashtrik_,

_Lorik_.

**Supervisor:**

_Prof. Blerim Rexha
&
Ass. Msc. Mergim Hoti_.

## Description

This project implements a Two-Factor Authentication (2FA) system, providing an additional layer of security for user logins. The system supports multiple methods of authentication, including:

- SMS-based codes
- Time-based One-Time Passwords (TOTP)
- Hardware tokens

The project is developed in Python using Flask for the web framework and integrates libraries such as `pyotp` for TOTP generation and `twilio` for sending SMS codes. The goal is to create a secure and user-friendly 2FA system that enhances the security of user accounts by requiring two forms of verification.

## How to Use

1. **Clone the repository to your local machine:**
    ```bash
    git clone https://github.com/l0rikkelmendi/SiguriDhenave_P3
    ```

2. **Navigate to the project directory:**
    ```bash
    cd 2FA_System
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the main Python script:**
    ```bash
    python 2FA.py
    ```

5. **Follow the on-screen prompts:**
    - Register a new user by providing a username and password.
    - Enable 2FA by entering a phone number to receive SMS codes or by setting up TOTP using a QR code.
    - Log in and verify using the chosen 2FA method.

## Results

The 2FA system successfully implements additional security measures by generating and validating one-time passwords (OTPs) via SMS or TOTP. Users can enable 2FA during registration or later through their profile settings. The system ensures that only authenticated users can access sensitive information, enhancing overall security.

## Expectations

By using this project, developers and security enthusiasts can learn about implementing 2FA in web applications. They can explore the integration of different authentication methods and understand best practices for securing user accounts. Additionally, the codebase can be extended for additional features or integrated into other software projects to improve security.

## Acknowledgments

We would like to thank Prof. Blerim Rexha & Ass. Msc. Mergim Hoti for their guidance and support throughout this project. Their expertise in cybersecurity has been invaluable in helping us navigate the complexities of implementing secure authentication systems.

▁▂▃▄▅▆▇▇▆▅▄▃▁▂▁▂▃▄▅▆▇▇▆▅▄▃▁▂
