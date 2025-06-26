import pyautogui
import time

def click_print_button(image_path="images/print_button.png", timeout=10, save_dir=None, filename=None, address_bar_coords=(300, 50)):
    """
    Click nút print bằng hình ảnh, sau đó thao tác popup Save As để lưu file.
    
    - image_path: đường dẫn ảnh nút print
    - timeout: thời gian tối đa tìm nút print (giây)
    - save_dir: thư mục lưu file (ví dụ: "D:\\InvoiceRPA\\results")
    - filename: tên file (ví dụ: "invoice.pdf")
    - address_bar_coords: tọa độ thanh địa chỉ popup Save As (x, y)
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if button_location:
            pyautogui.moveTo(button_location)
            pyautogui.click()
            
            if save_dir and filename:
                time.sleep(2)  # Chờ popup Save As hiện ra
                
                # # Click vào thanh địa chỉ để nhập đường dẫn thư mục
                # pyautogui.click(address_bar_coords[0], address_bar_coords[1])
                # time.sleep(0.5)
                
                # # Xóa nội dung thanh địa chỉ (Ctrl+A, Delete)
                # pyautogui.hotkey('ctrl', 'a')
                # time.sleep(0.2)
                # pyautogui.press('delete')
                # time.sleep(0.2)
                
                # Gõ đường dẫn thư mục rồi Enter
                pyautogui.write(save_dir)
                pyautogui.press('enter')
                time.sleep(1)  # Đợi chuyển thư mục
                
                # Gõ tên file
                pyautogui.write(filename)
                time.sleep(0.5)
                
                # Nhấn Enter để lưu file
                pyautogui.press('enter')
                time.sleep(2)  # Đợi lưu file hoàn tất
                
            return True
        time.sleep(0.5)
    raise Exception(f"Không tìm thấy nút print với ảnh {image_path} trong {timeout} giây.")
