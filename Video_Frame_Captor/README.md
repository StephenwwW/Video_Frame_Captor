# Video Frame Captor

**[English](#english-version) | [繁體中文](#繁體中文版)**

A simple GUI tool to batch extract frames from video files (`.mov`, `.mp4`) at specified timestamps. Built with Python, PyQt6, and OpenCV.

一個簡單的圖形化工具，可以用來在指定的時間點，批次從影片檔案（`.mov`, `.mp4`）中擷取畫格。使用 Python、PyQt6 和 OpenCV 打造。

---

## English Version

### Screenshot

![Screenshot of Video Frame Captor](https://raw.githubusercontent.com/StephenwwW/Video_Frame_Captor/main/Video_Frame_Captor/images/screenshot.png)

### Features

-   **User-Friendly GUI**: Simple and intuitive interface with language switching (English/Traditional Chinese).
-   **Batch Processing**: Process all videos (`.mov`, `.mp4`) in a selected folder automatically.
-   **Custom Timestamps**: Specify multiple timestamps (in seconds, including decimals) to capture frames from.
-   **Robust File Handling**: Supports file paths with non-ASCII characters.
-   **Smart Output**: Automatically creates an `images` subfolder inside your target folder.
-   **Standalone Executable**: Includes a batch script to build a single `.exe` file using PyInstaller and UPX.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/StephenwwW/Video-Frame-Captor.git
    cd Video-Frame-Captor
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application from source:**
    ```bash
    python video_frame_captor.py
    ```

### Building the Executable (`.exe`)

This project includes a `build_video_frame_extractor.bat` script to simplify the process of packaging the application into a single `.exe` file using `PyInstaller`. It also supports `UPX` to reduce the final file size.

**1. Prerequisites:**
   - Install PyInstaller: `pip install pyinstaller`
   - **(Optional) Download UPX:** For file compression, download the latest win64 version of UPX from the official GitHub releases page:
     [**UPX Official Releases**](https://github.com/upx/upx/releases)
   - After downloading, extract the `upx-x.x.x-win64` folder and place it on your desktop. The batch script expects it at `C:\Users\YourUsername\Desktop\upx-x.x.x-win64`. You may need to edit the path inside the `.bat` file.

**2. Run the Build Script:**
   - Double-click `build_video_frame_extractor.bat`.
   - You will be prompted to choose a build method:
     1.  **`--onefile --noconsole --upx-dir`**: Standard build with UPX compression. Recommended.
     2.  **`--onefile --noconsole`**: Build without UPX compression. The file will be larger.
     3.  **`--onefile --noconsole --strip --clean --upx-dir`**: Clean build with UPX, removing temporary files before building.
   - Enter your choice (1, 2, or 3) and press Enter.

**3. Get the Output:**
   - After the script finishes, the final `video_frame_extractor.exe` file will be moved to a `Video_Frame_Captor` folder on your Desktop.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/StephenwwW/Video_Frame_Captor/blob/main/Video_Frame_Captor/LICENSE) file for details.

---
## 繁體中文版

### 軟體截圖

![影片畫格擷取工具截圖](https://raw.githubusercontent.com/StephenwwW/Video_Frame_Captor/main/Video_Frame_Captor/images/screenshot.png)

### 功能特性

-   **友善的圖形介面**：簡單直觀，並支援中英雙語切換。
-   **批次處理**：自動處理選定資料夾中的所有影片（`.mov`, `.mp4`）。
-   **自訂時間點**：可指定多個擷取時間點（單位為秒，支援小數）。
-   **強大的檔案處理**：支援包含特殊字元（如中文、日文）的檔案路徑。
-   **智慧化輸出**：自動在您選擇的目標資料夾內建立 `images` 子資料夾。
-   **獨立執行檔**：內附批次檔，可使用 PyInstaller 與 UPX 打包成單一 `.exe` 檔。

### 安裝與執行 (開發者適用)

1.  **複製專案倉庫：**
    ```bash
    git clone https://github.com/StephenwwW/Video-Frame-Captor.git
    cd Video-Frame-Captor
    ```
    
2.  **建立虛擬環境（建議）：**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **安裝所需套件：**
    ```bash
    pip install -r requirements.txt
    ```

4.  **從原始碼執行應用程式：**
    ```bash
    python video_frame_captor.py
    ```

### 打包為執行檔 (`.exe`)

本專案內含一個 `build_video_frame_extractor.bat` 批次檔，用以簡化 `PyInstaller` 的打包流程，並可選用 `UPX` 壓縮工具來縮小最終檔案體積。

**1. 前置準備：**
   - 安裝 PyInstaller：`pip install pyinstaller`
   - **(選擇性) 下載 UPX：** 若要壓縮檔案，請至 UPX 官方 GitHub 發布頁面下載最新的 win64 版本：
     [**UPX 官方發布頁**](https://github.com/upx/upx/releases)
   - 下載後，將解壓縮的 `upx-x.x.x-win64` 資料夾放在您的桌面。批次檔預期路徑為 `C:\Users\您的使用者名稱\Desktop\upx-x.x.x-win64`，您也可以自行編輯 `.bat` 檔內的 `UPX` 路徑。

**2. 執行打包腳本：**
   - 直接雙擊執行 `build_video_frame_extractor.bat`。
   - 腳本會提示您選擇打包方式：
     1.  **`--onefile --noconsole --upx-dir`**：標準打包，使用 UPX 壓縮。推薦此項。
     2.  **`--onefile --noconsole`**：不使用 UPX 壓縮，檔案會比較大。
     3.  **`--onefile --noconsole --strip --clean --upx-dir`**：使用 UPX 清理打包，會在建置前移除暫存檔。
   - 輸入您的選擇 (1, 2, 或 3) 後按下 Enter。

**3. 取得成品：**
   - 腳本執行完畢後，最終生成的 `video_frame_extractor.exe` 會被移動到您桌面的 `Video_Frame_Captor` 資料夾內。

### 授權條款

本專案採用 MIT 授權條款 - 詳細資訊請參閱 [LICENSE](https://github.com/StephenwwW/Video_Frame_Captor/blob/main/Video_Frame_Captor/LICENSE)檔案。
