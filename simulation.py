import csv
import queue

class Request:
    def __init__(self, time, process_time):
        self.timestamp = time
        self.process_time = process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None

    def busy(self):
        return self.current_request is not None

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.process_time

def simulateOneServer(file_name):
    server = Server()
    request_queue = queue.Queue()
    waiting_times = []

    # Reading the requests from the CSV file
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            #  CSV format is [time, file_name, process_time]
            request = Request(int(row[0]), int(row[2]))
            request_queue.put(request)

    current_second = 0
    while not request_queue.empty():
        if (not server.busy()) and (not request_queue.empty()):
            next_request = request_queue.get()
            waiting_times.append(next_request.wait_time(current_second))
            server.start_next(next_request)

        server.tick()
        current_second += 1

    average_wait = sum(waiting_times) / len(waiting_times)
    print(f"Average Wait {average_wait:.2f} secs. {len(waiting_times)} tasks processed.")


def main():
    # CSV file
    file_path = "C:\\Users\\faruk\\Downloads\\requests.csv"
    simulateOneServer(file_path)

if __name__ == "__main__":
    main()
