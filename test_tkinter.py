import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import random

def while_list(orig_list, max_attempts=100):

    random.shuffle(orig_list)
    list1 = [f"{i + 1}.{value}" for i, value in enumerate(orig_list)]
    
    for attempts in range(max_attempts):
        new_list = random.sample(list1, len(list1))  # 隨機抽取完整列表
        if all(orig != new for orig, new in zip(list1, new_list)):  # 確保沒有抽到自己
            return new_list  # 返回有效的抽取結果

    return None  # 如果達到最大嘗試次數後仍無法找到有效結果


def random_select(orig_list):
    # 隨機抽取一個不重複的列表，確保沒有元素抽到自己
    
    new_list = while_list(orig_list, max_attempts=100)
    #print(new_list)
    # 用 replace 處理全形和半形冒號，並將列表轉換成字典
    #index_mapping = {idx: {new_list.index(value):value} for idx, value in enumerate(list1)}
    index_mapping = {orig_idx: {value: new_list[orig_idx]} for orig_idx, value in enumerate(orig_list)}

    #print(index_mapping)
    return index_mapping

# 定義發送郵件的函數
def send_email():
    
    sender_email = "boli.1004o0@gmail.com"  # 寄件人 Email
    sender_password = "wexi cvig huon rnqi"        # 寄件人 Email 密碼（建議使用應用程式密碼）
    #receiver_email = email_entry.get()       # 取收件人的 Email
    #receiver_email = 'cks012340@gmail.com'
    subject = subject_entry.get()            # 取郵件主題
    # body = body_text.get("1.0", tk.END)      # 取郵件內容
    # 获取文本框的所有内容
    content = body_text.get("1.0", tk.END).strip()  # 去除结尾的多余换行符
    # 根据换行符分隔内容，形成列表
    content_list = content.splitlines()
    #print(content_list)  # 输出结果，或者可以在其他地方使用
    index_mapping = random_select(content_list)

    for key,value in index_mapping.items():
        print('key,value')
        print(key,value)
        for sub_k,sub_v in value.items():
            #print('sub_k,sub_v')
            #print(sub_k,sub_v)
            receiver_email = sub_k.split(':')[1]
            body = f'Hi, \n恭喜抽到{sub_v.split(':')[0]}! 準備好您的500到1000塊買一個酷酷的禮物送他!'
        with open('MariahCarey.jpg','rb') as file:
            image_data = file.read()
        img = MIMEImage(image_data,name = 'MariahCarey.jpg')
        if not receiver_email or not subject or not body:
            messagebox.showerror("錯誤", "所有欄位都是必填的")
            return

        # 構建郵件
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        msg.attach(img)

        try:
            # 設定 SMTP 伺服器（此處以 Gmail 為例）
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # 開啟加密傳輸
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            #messagebox.showinfo("成功", "郵件已成功發送！")
        except Exception as e:
            messagebox.showerror("錯誤", f"郵件發送失敗: {e}")
    messagebox.showinfo("成功", "郵件已成功發送！")
# 建立 tkinter 窗口
root = tk.Tk()
root.title("寄信程式")

# Email 輸入欄
#tk.Label(root, text="收件人 Email:").grid(row=0, column=0, padx=10, pady=10)
#email_entry = tk.Entry(root, width=50)
#email_entry.grid(row=0, column=1, padx=10, pady=10)

# 主題輸入欄
tk.Label(root, text="郵件主題:").grid(row=1, column=0, padx=10, pady=10)
subject_entry = tk.Entry(root, width=50)
subject_entry.grid(row=1, column=1, padx=10, pady=10)

# 郵件內容輸入欄
tk.Label(root, text="請填入(人名:email)\n並按enter新增下一位").grid(row=2, column=0, padx=10, pady=10)
body_text = tk.Text(root, height=10, width=50)
body_text.grid(row=2, column=1, padx=10, pady=10)

# 發送按鈕
send_button = tk.Button(root, text="發送郵件", command=send_email)
send_button.grid(row=3, column=1, pady=20)

# 開始主迴圈
root.mainloop()