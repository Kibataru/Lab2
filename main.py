import os
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def lab():
    inp = 'product.csv'
    out = 'output.json'
    result = []

    with open(inp, mode='r', encoding='utf-8') as f:
        a = csv.DictReader(f)
        products = list(a)

    for i in products:
        i_id = i['id']
        des = i['description']

        prompt = (
            "Ты извлекаешь данные из текста три характеристики товара: "
            "brand (бренд), category (категория) и price (цена) "
            "При отсутствии чего-либо, пиши null "
            "Фомат вывода json "
        )

        completion = client.chat.completions.create(
            model="mimo-v2.5-pro",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": des}
            ],
            temperature=0.0,
            max_tokens=512
        )

        final = completion.choices[0].message.content
        answer = json.loads(final)
        answer['id'] = i_id
        result.append(answer)

    with open(out, mode='w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    lab()