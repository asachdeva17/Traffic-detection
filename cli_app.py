from trafficdetection import video_count
import os

def main_menu():
    print("==========================================")
    print("  Traffic Congestion Detector")
    print("==========================================")
    print("Analyses a traffic video and rates congestion")
    print("as Low, Medium or High for each time interval.")
    print()

def show_options():
    print("1. Analyse a video")
    print("2. Exit")

def path_input():
    while True:
        path = input("Enter the path of the video file: ")
        if os.path.isfile(path):
            return path
        print("File not found. Check the path and try again.")

def main():
    main_menu()
    while True:
        show_options()
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            path = path_input()
            print("Video selected:", path)
        elif choice == "2":
            print("Thank you. Have a nice day!")
            break
        else:
            print("Please enter 1 or 2.")
        print()

if __name__ == "__main__":
    main()