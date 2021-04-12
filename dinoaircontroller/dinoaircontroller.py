import cv2, pyautogui

def start():
    cap = cv2.VideoCapture(0)
    frame_count = 0
    spot_jump = 0
    spot_crawl = 0

    while True:
        frame_count += 1
        ret0, frame = cap.read()
        ret, frame0 = cap.read()
        crop_img_dummy1 = frame0[250:300, 5:55]
        crop_img1 = frame[250:300, 5:55]
        crop_img_dummy2 = frame0[250:300, 585:635]
        crop_img2 = frame[250:300, 585:635]
        cv2.rectangle(frame, (5, 250), (55, 300), (255, 0, 0), 3)
        cv2.rectangle(frame, (585, 250), (635, 300), (255, 0, 0), 3)
        cv2.putText(frame, "CRAWL", (555, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.putText(frame, "JUMP", (5, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        diff1 = cv2.absdiff(crop_img_dummy1, crop_img1)
        diff2 = cv2.absdiff(crop_img_dummy2, crop_img2)
        gray1 = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)
        blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        _, thresh1 = cv2.threshold(blur1, 20, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(blur2, 20, 255, cv2.THRESH_BINARY)
        dilated1 = cv2.dilate(thresh1, None)
        dilated2 = cv2.dilate(thresh2, None)
        contours1, _ = cv2.findContours(dilated1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(dilated2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if spot_jump == 0:
            for contour in contours1:
                if cv2.contourArea(contour) <= 50:
                    pyautogui.press('space')
                    spot_jump = 5
        else:
            cv2.putText(frame, "Jumping", (250, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            spot_jump -= 1
        if spot_crawl == 0:
            for contour in contours2:
                if cv2.contourArea(contour) <= 50:
                    pyautogui.keyDown('down')
                    spot_crawl = 15
        else:
            cv2.putText(frame, "Crawling", (250, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            spot_crawl -= 1
            if spot_crawl == 1:
                pyautogui.keyUp('down')
        cv2.imshow("aaa", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
