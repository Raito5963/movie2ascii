import sys
import cv2
import msvcrt

ascii_chars = ".-=:+#%@"

def frame_to_ascii(frame, width, color):
    h,w,_ = frame.shape
    height = int(width * (h/w) * 0.5)

    resized = cv2.resize(frame, (width, height))

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    ascii_lines = []
    num_chars = len(ascii_chars)


    for y in range(height):
        line = []
        for x in range(width):
            lum = gray[y,x]
            char = ascii_chars[int(lum / 256*num_chars)]

            if color == "color":
                b, g, r = resized[y, x]
                line.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
            else:
                line.append(char)

        ascii_lines.append("".join(line))
    return "\n".join(ascii_lines)

def main():
    global ascii_chars
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error")
        return

    color = "color"
    width = 120

    print("[c] change color / mono | [r] reverse ascii | [q] quit")

    sys.stdout.write("\033[2J\033[?25l")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            sys.stdout.write("\033[H")

            ascii_frame = frame_to_ascii(frame, width, color)
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b"q", b"Q"):
                    break
                elif key in (b"r", b"R"):
                    ascii_chars = ascii_chars[::-1]
                elif key in (b"c", b"C"):
                    color = "mono" if color == "color" else "color"

    finally:
        sys.stdout.write("\033[?25h\033[0m\n")
        cap.release()

if __name__ == "__main__":
    main()