from trafficdetection import video_count

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

def main():
    main_menu()
    while True:
        show_options()
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            print("Analysis loop test.")
        elif choice == "2":
            print("Thank you. Have a nice day!")
            break
        else:
            print("Please enter 1 or 2.")
        print()

if __name__ == "__main__":
    main()