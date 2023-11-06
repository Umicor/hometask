import os
import time
import threading
import multiprocessing
import requests
#time.sleep(5) для имитации тяжелой вычислительной задачи.
# CPU-bound task (simulated heavy computation)
def encrypt_file(path: str):
    print(f"Processing file {path} in process {os.getpid()}")
    # Simulate heavy computation by sleeping for a while
    time.sleep(5)  # Замените на реальную тяжелую задачу, например, на ваше шифрование

# I/O-bound task (downloading image from URL)
def download_image(image_url):
    print(f"Downloading image from {image_url} in thread {threading.current_thread().name}")
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)

if __name__ == "__main":
    start_time = time.perf_counter()

    try:
        # Создайте отдельные потоки и процессы для выполнения задач
        encryption_thread = threading.Thread(target=encrypt_file, args=("rockyou.txt",))
        download_process = multiprocessing.Process(target=download_image, args=("https://picsum.photos/1000/1000",))

        encryption_thread.start()
        download_process.start()

        encryption_thread.join()
        download_process.join()

    except Exception as e:
        print(f"Error occurred: {e}")

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")

