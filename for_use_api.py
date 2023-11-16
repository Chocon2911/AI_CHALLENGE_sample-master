import openai
import argparse
import time 
import re

from dataset import get_data



def get_response(args, user_request, max_len, temp):
    responese = openai.Completion.create(
        engine = args.model_name,
        prompt = user_request,
        max_tokens = max_len,
        n = 1,
        temperature = temp
    )

    return responese

def convert_to_submit_file(api_result: list = []):
    answer_start = api_result.find("Answer: ")
    if answer_start != -1:
        answer_end = api_result.find(",", answer_start)
        answer_part = api_result[answer_start + len("Answer: "):answer_end]

        if any(c.isalpha() for c in answer_part):
            answer = answer_part[0:answer_part.find(")")]  
        else:
            answer = answer_part
        return answer.lower()
    else:
        answer = api_result
        return answer.lower()
    return 'Nan'
            
                

def main(args):
    print(args)
    with open("openai_api_key.txt", "r") as f:
        openai.api_key = f.readline()
        test_examples = get_data(args.data)
        results = []
        with open('./results/results.txt', 'r') as read:
            results = read.readlines()
        curr_indx = 1
        last_indx = len(results)
        print("Last request: ", last_indx)
        with open('./results/results.txt', 'a') as f:
            for problem in test_examples:
                prompt = """
                Assume that you are doing a SAT Test. 
                This is an example (multiple choices question format) of the question you need to answer:
                "id": 2,
                "Problem": "a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?",
                "options": "a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650",
                "diagramRef": "",
                "category": "general"
                Your answer format should be like this:
                Answer: c
                """

                ques = problem["Problem"]
                max_len = 2000
                temp = 0.2
                user_request = prompt + ques
                responese = {}
                if curr_indx > last_indx:
                    while 'id' not in responese:
                        try:
                            print("try")
                            t1 = time.time()
                            responese = get_response(args, user_request, max_len, temp)
                            #print(user_request)
                            t2 = time.time()
                            time_request = t2 - t1
                            answer = responese.choices[0].text
                            #results.append([answer, time_request])
                        except:
                            print("Waiting...")
                            time.sleep(20)
                            continue
                    print(f"Time request for {problem['id']}: {time_request}, answer: {answer}")
                    choose = convert_to_submit_file(answer)
                    f.write(choose + '\t' + str(time_request) + '\n')
                    
                curr_indx += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
		"--model_name", type=str, 
		default="text-davinci-003",
        help= "Name to request model from openai"
	)
    parser.add_argument(
		"--data", type=str, 

		default="./data/test.json",
		help="Path to data test"
	)

    args = parser.parse_args()
    print(args)
    main(args)
