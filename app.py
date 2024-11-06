# app.py
import streamlit as st
from langchain_openai import ChatOpenAI
from crewai import Crew, Process
import os