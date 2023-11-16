import openai

# Thay thế bằng khóa API của bạn
api_key = 'AIzaSyCHiGM1hj7l1hsEN1sUmPqKfQMPV6lmMPY'

# Dữ liệu câu hỏi và tùy chọn
training_data = [
    {
        "id": 1,
        "Problem": "for a certain exam , a score of 58 was 2 standard deviations below mean and a score of 98 was 3 standard deviations above mean . what was the mean score w for the exam ?",
        "options": "a ) 74 , b ) 76 , c ) 78 , d ) 80 , e ) 82",
    },
    {
        "id": 2,
        "Problem": "a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?",
        "options": "a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650",
    }
]

# Chuyển đổi dữ liệu thành định dạng yêu cầu bởi API
training_samples = []
for item in training_data:
    problem = item["Problem"]
    options = item["options"]
    training_samples.append(f"Question: {problem}\nOptions: {options}\n")

# Tạo dữ liệu đào tạo
training_text = "\n".join(training_samples)

# Gửi dữ liệu đào tạo đến API
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=training_text,
    max_tokens=150,  # Số lượng tokens tối đa cho mỗi câu trả lời
    n=1,              # Số câu trả lời bạn muốn
    stop=None,        # Dừng khi gặp ký tự mới (không bắt buộc)
    temperature=0.7,  # Điều chỉnh độ đa dạng của câu trả lời
    api_key=api_key
)

# Hiển thị câu trả lời từ mô hình
print(response.choices[0].text)
