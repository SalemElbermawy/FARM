# AI Farming Disease Detection System

## Overview
This project is an AI-based system for detecting plant diseases from images.  
It classifies plant conditions into three categories:
- Early Blight
- Late Blight
- Healthy

The system combines computer vision and language models to provide accurate predictions along with meaningful explanations.

## System Architecture
The system follows this pipeline:

Input Image  
→ CNN Model (Classification)  
→ LLM (Image Understanding)  
→ RAG (Research Retrieval)  
→ LLM (Final Response Generation)  
→ Output (Diagnosis + Explanation)

## Components

### CNN Model
- Performs image classification
- Outputs one of the three classes

### LLM
- Interprets model predictions
- Generates human-readable explanations

### RAG System
- Retrieves relevant information from research papers
- Enhances response with scientific knowledge

### Final Response
- Combines prediction and retrieved data
- Provides explanation, causes, and recommendations

## Technologies
- Python
- CNN (Deep Learning) 
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)

## To be loyal with that , I have used AI to write the prompts 
