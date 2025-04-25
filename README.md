Hello World!

# 🔍 Calibre Plugin Security Assessment

This project provides a comprehensive security analysis of Calibre, a widely used open-source e-book management software. Our focus is on evaluating the security posture of its plugin architecture using static analysis tools and formal threat modeling techniques.

---

## 📚 Project Overview

Calibre is a feature-rich e-book manager with a robust plugin system that allows users to extend functionality. However, this modularity can introduce potential vulnerabilities if plugins are insecurely developed or poorly isolated. This project investigates the security of Calibre’s plugin layer, identifying risks that could affect user data, application stability, or system integrity.

---

## 🎯 Objectives

- Evaluate Calibre’s plugin system for vulnerabilities and misconfigurations
- Apply threat modeling techniques (STRIDE, DREAD) to assess risk
- Perform static code analysis using Bandit and Pylint
- Provide actionable recommendations to improve Calibre's security

---

## 🧪 Environment Setup

To reproduce our analysis:

We set up Visual Studio Code in an Ubuntu Linux Virtual Machine. Once you have that set up you can just copy our scripts and run calibre_plugin_analyzer.py first to create a clone of Calibres GitHub Repository and scan the found plugin files woth Bandit and pylint.

The other scripts are used for data formatting and consolidation for a prpject review.
