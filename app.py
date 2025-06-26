import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import traceback  # <-- Thêm nếu chưa có
import os

app = Flask(__name__)
CORS(app)  # Cho phép gọi API từ frontend bất kỳ (hoặc bạn có thể cấu hình cụ thể)

def run_robot(invoice_code):
    cmd = [
        "python", "-m", "robot",
        "--variable", f"INVOICE_CODE:{invoice_code}",
        "InvoiceDownload.robot"
    ]
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print("Robot stdout:", process.stdout)
        print("Robot stderr:", process.stderr)
        print("Return code:", process.returncode)
        return process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired:
        print("Robot chạy timeout")
        return "", "Robot Framework chạy quá thời gian cho phép", -1
    except Exception as e:
        print("Lỗi khi chạy Robot Framework:", str(e))
        return "", f"Lỗi khi chạy Robot Framework: {str(e)}", -2


PDF_DIR = r"D:\InvoiceRPA\results"
@app.route('/api/download_pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    try:
        return send_from_directory(PDF_DIR, filename, as_attachment=False)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/api/list_pdfs', methods=['GET'])
def list_pdfs():
    try:
        if not os.path.exists(PDF_DIR):
            os.makedirs(PDF_DIR)

        files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith('.pdf')]
        return jsonify({"status": "success", "files": files})
    except Exception as e:
        print("❌ Lỗi trong list_pdfs:", str(e))
        traceback.print_exc()  # <-- In chi tiết stacktrace ra terminal
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/api/download_invoice', methods=['POST'])
def download_invoice():
    try:
        data = request.json
        invoice_code = data.get('invoice_code')
        if not invoice_code:
            return jsonify({"status": "error", "message": "Thiếu mã tra cứu"}), 400

        stdout, stderr, rc = run_robot(invoice_code)

        if rc == 0:
            return jsonify({
                "status": "success",
                "message": "Hoàn tất chạy Robot Framework",
                "robot_log": stdout
            })
        elif rc == -1:
            return jsonify({"status": "error", "message": "Robot Framework chạy timeout"}), 504
        elif rc == -2:
            return jsonify({"status": "error", "message": "Lỗi nội bộ khi chạy Robot"}), 500
        else:
            return jsonify({
                "status": "error",
                "message": "Robot Framework chạy lỗi",
                "robot_error": stderr
            }), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Lỗi server: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
