import json
import os
import streamlit as st

TESTS_DIR = "tests"

st.set_page_config(
    page_title="Литовско-русский языковой тест", page_icon="🇱🇹", layout="centered"
)

st.header("🇱🇹 Литовско-русский языковой тест")


def load_test_list():
  if not os.path.exists(TESTS_DIR):
    return []
  files = [f for f in os.listdir(TESTS_DIR) if f.endswith(".json")]
  return sorted(files)


def load_test(test_file):
  file_path = os.path.join(TESTS_DIR, test_file)
  with open(file_path, "r", encoding="utf-8") as f:
    return json.load(f)


test_files = load_test_list()

if not test_files:
  st.warning("Пока нет доступных тестов. Обратитесь к преподавателю.")
else:
  selected_file = st.selectbox(
      "Выберите тест для прохождения:",
      test_files,
      format_func=lambda x: x.replace(".json", ""),
  )

  if selected_file:
    test_data = load_test(selected_file)

    with st.form("quiz_form"):
      user_answers = {}
      for i, q in enumerate(test_data):
        st.markdown(f"### Вопрос {i+1}")
        st.write(q["question"])

        if q["type"] == "Выбор из вариантов":
          user_answers[i] = st.radio("Выберите ответ:", q["options"], key=f"q_{i}")
        else:
          user_answers[i] = st.text_input("Ваш ответ:", key=f"q_{i}").strip()

        st.write("---")

      submitted = st.form_submit_button("✅ Отправить ответы")

      if submitted:
        score = 0
        total = len(test_data)
        for i, q in enumerate(test_data):
          user_ans = str(user_answers[i]).strip().lower()
          correct_ans = str(q["answer"]).strip().lower()

          if user_ans == correct_ans:
            score += 1

        st.balloons()
        st.success(f"Тест завершен! Ваш результат: **{score} из {total}**")