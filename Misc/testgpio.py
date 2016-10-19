import RPi.GPIO as GPIO

def main():
    print("Starting LED-io")

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)

    print("\nEnter an option:\n1 - Turn on LED\n2 - Turn off LED\n0 - Quit\nOption: ")

    option = input()

    while option != 0:
        # print("\n\nOption: ")
        # print(option)
        # print("\n\n")
        if option == 1:
            GPIO.output(17, True)
        elif option == 2:
            GPIO.output(17, False)
        option = input("Enter option again: ")

    GPIO.cleanup()

if __name__=="__main__":
    try:   
        main()
    except:
        GPIO.cleanup()
