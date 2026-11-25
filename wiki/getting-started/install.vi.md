---
title: Cài đặt và kiểm tra PSE
description: Cài một bản PSE đã checkout và xác thực môi trường Python và LuaLaTeX cục bộ.
---

# Cài đặt và kiểm tra PSE

PSE hiện hướng tới Windows, macOS và Linux. Bạn cần **Python 3.11 trở lên** và một bản phân phối TeX có **LuaLaTeX**. Bộ cài đặt của PSE không cài bản phân phối TeX cho bạn.

## Cài một bản phân phối TeX

PSE dàn trang sách bằng **LuaLaTeX**, có sẵn trong mọi bản phân phối TeX đầy đủ. Chọn một trong:

- **Windows:** cài [MiKTeX](https://miktex.org) hoặc [TeX Live](https://tug.org/texlive/), rồi bảo đảm lệnh `lualatex` nằm trên PATH (bộ cài đã làm sẵn việc này).
- **macOS:** cài [MacTeX](https://tug.org/mactex/), bản macOS của TeX Live.
- **Linux (Debian/Ubuntu):** cài các gói bằng `sudo apt-get install`:

```text
sudo apt-get install --no-install-recommends \
  texlive-luatex texlive-latex-extra texlive-fonts-recommended \
  texlive-bibtex-extra biber
```

Sách có tiếng Hy Lạp hay hệ chữ khác ngoài Latin nên cài thêm một phông hỗ trợ đầy đủ đa dấu. PSE dùng **Gentium Plus** theo mặc định; trên Linux đó là gói `fonts-sil-gentiumplus`, và TeX Live cài sẵn nó trên Windows và macOS.

Sau khi cài, xác minh `pse doctor` báo LuaLaTeX sẵn sàng trước khi tiếp tục.

## Cài từ kho đã checkout

Mở terminal ở thư mục gốc kho PSE và chạy:

```text
python -m pip install .
pse doctor --deep
```

`pse doctor --deep` kiểm tra môi trường đã cài và thực hiện một lần tạo lập LuaLaTeX an toàn tạm thời. Chỉ tiếp tục khi các kiểm tra bắt buộc đạt. Các cảnh báo tư vấn về công cụ soát tùy chọn khác với các lỗi bắt buộc.

## Lựa chọn bootstrap được quản lý

Nếu bạn không muốn tự quản môi trường Python, kho cũng cung cấp các script bootstrap. Trên macOS/Linux, từ thư mục gốc kho:

```text
./scripts/bootstrap/unix-install.sh
```

Trên Windows PowerShell:

```text
.\scripts\bootstrap\windows-install.ps1 -AddToPath
```

Sau mỗi lộ trình, chạy:

```text
pse doctor --deep
```

## Thành công nghĩa là gì

Một lần doctor thành công cho bạn biết máy trạm có thể chạy đường cơ sở PSE một cách an toàn. Nó **không** chứng nhận một bản thảo, một bố cục hay một PDF cuối cùng cụ thể. Những kiểm tra đó diễn ra ở cấp dự án.

Tiếp: [Chọn hồ sơ trình bày](choose-a-profile.md).
