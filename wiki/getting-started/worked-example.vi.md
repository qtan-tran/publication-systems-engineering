---
title: Một ví dụ làm trọn vẹn
description: Tạo lập một giáo trình tiếng Hy Lạp cổ năm chương với hình minh họa thuộc phạm vi công cộng, từ một thư mục trống đến một tệp PDF đã kiểm tra.
---

# Một ví dụ làm trọn vẹn: giáo trình tiếng Hy Lạp cổ

Trang này đi trọn con đường của [Cẩm nang cho người mới](index.md) trên một dự án thật, đã hoàn thành: một giáo trình nhập môn năm chương dạy tiếng Hy Lạp cổ, với hai bức ảnh và một bản chụp bản thảo cổ làm minh họa. Mọi lệnh dưới đây là một dòng bạn dán vào terminal, và mọi lần sửa tệp là biên tập văn bản thông thường. Không liên quan đến lập trình.

Dự án hoàn thành được công bố trong kho PSE, nên bạn có thể so sánh sản phẩm của mình với nó ở bất kỳ điểm nào: <https://github.com/qtan-tran/publication-systems-engineering/tree/main/examples/tutorials/greek-textbook>. Các chương của nó cố tình ngắn để cả cuốn sách vừa trong một màn hình chú ý của bạn.

## Cuốn sách hoàn thành chứa gì

- năm chương, mỗi chương trong một tệp riêng dưới `content/`: vì sao học tiếng Hy Lạp, bảng chữ cái, danh từ đầu tiên, thời hiện tại, và lần đọc đầu tiên tiếng Hy Lạp thật;
- một mục lục mà PSE tự tạo, một chỉ mục các thuật ngữ then chốt, và một trang Ghi nhận Hình ảnh ở phần cuối;
- tiếng Hy Lạp cổ đa dấu được dàn bằng một phông Hy Lạp đầy đủ, nên dấu thanh và dấu hơi hiển thị đúng;
- ba hình minh họa thuộc phạm vi công cộng từ Wikimedia Commons;
- một PDF được sản xuất và kiểm tra bằng máy với đúng các lệnh trình bày trên trang này.

## Bước 0. Chuẩn bị máy trạm

Làm theo [Cài đặt và kiểm tra PSE](install.md) trước, và dừng lại sau khi `pse doctor` đạt. Bạn cần kết nối internet để tải hình ở Bước 3.

## Bước 1. Tạo dự án

Tạo dự án trong **bộ nhớ riêng tư**, ngoài kho PSE. Trong terminal, chạy:

```text
pse new /path/to/private-projects \
  --profile academic-monograph \
  --title "Ancient Greek for Beginners" \
  --author "Alexandros Didaskalos" \
  --language en \
  --publication-year 2027 \
  --slug greek-textbook \
  --non-interactive
```

Trên PowerShell, hãy đặt lệnh trên một dòng thay vì dùng cách nối dòng bằng gạch chéo như trên.

Hai ghi chú riêng cho cuốn sách này:

- `academic-monograph` là hồ sơ được hỗ trợ cho giáo trình và mọi phi hư cấu có cấu trúc. Nếu bạn đang tìm một hồ sơ tên `academic-book` hay `textbook`, thì đây là hồ sơ cần dùng.
- Các tùy chọn trong lệnh là cùng những giá trị mà bộ sinh hỏi tương tác khi bạn bỏ chúng đi. `--non-interactive` bỏ qua các câu hỏi, cũng là lựa chọn đúng khi terminal không hỏi được (chẳng hạn trong một script).

`pse new` in ra thư mục nó đã tạo; hãy chuyển vào đó. Rồi mở `book.yml` trong trình soạn thảo và thêm một dòng siêu dữ liệu nữa dưới `title`:

```text
subtitle: A Complete Textbook
```

## Bước 2. Viết các chương

Bộ sinh tạo các chương khởi đầu. Một chương là một tệp văn bản thuần, `content/chapter-01.tex`, `content/chapter-02.tex`, v.v. Mở từng tệp và thay văn bản khởi đầu bằng của bạn, giữ cùng hình dạng đơn giản:

- tệp bắt đầu bằng tiêu đề chương, chẳng hạn `\chapter{Why Learn Ancient Greek?}`;
- các đoạn văn là những dòng văn bản cách nhau bởi một dòng trống;
- một tiêu đề mục trong chương là `\section{...}` theo cùng kiểu;
- một chú thích cuối trang được bọc trong `\footnote{...}` tại nơi dấu chỉ ghi chú thuộc về.

Cuốn sách demo dùng năm chương: *Why Learn Ancient Greek?*, *The Alphabet and Sounds*, *First Nouns and the Article*, *The Present Tense*, và *Reading Real Greek*. Chương 2 chứa một bảng các chữ cái; Chương 3 biến cách danh từ `\PSEGreek{λόγος}`; hãy giữ bảng đúng như các tệp khởi đầu trình bày và chỉ thay chữ bên trong.

Cuối cùng, mở `main.tex` ở thư mục gốc dự án và đưa cho cuốn sách danh sách chương của nó: một dòng `\input` mỗi chương, theo thứ tự đọc, thay các dòng khởi đầu:

```tex
\input{content/chapter-01.tex}
\input{content/chapter-02.tex}
\input{content/chapter-03.tex}
\input{content/chapter-04.tex}
\input{content/chapter-05.tex}
```

Thứ tự chương là thứ tự của các dòng này; trước mắt không cần thay đổi gì khác trong `main.tex`.

## Bước 3. Thêm hình minh họa phạm vi công cộng

Tạo một thư mục tên `assets` ở thư mục gốc dự án nếu bộ sinh chưa tạo. Sau đó, từ thư mục gốc dự án, lấy ba hình minh họa mà bản demo dùng:

```text
curl -sL -o assets/parthenon-west.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Parthenon_from_west.jpg"
curl -sL -o assets/homer-bm-1825.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Bust%20Homer%20BM%201825.jpg"
curl -sL -o assets/greek-manuscript-6c.png "https://commons.wikimedia.org/wiki/Special:FilePath/Greek%20manuscript%20cursive%206th%20century.png"
```

Bạn cũng hoàn toàn có thể tải các hình bằng trình duyệt và lưu vào `assets`. Cả ba tác phẩm đều thuộc phạm vi công cộng, đó là lý do một cuốn sách có thể in lại chúng mà không cần quy trình xin phép. Dù dùng hình gì, chỉ giữ những hình bạn có quyền tái sản xuất, và ghi lại nguồn của từng hình.

Một hình ảnh vào chương như một khối figure. Khối này, từ Chương 1, đặt ảnh Parthenon cùng chú đề của nó:

```tex
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.86\linewidth]{assets/parthenon-west.jpg}
  \caption{The Parthenon on the Acropolis of Athens, seen from the west.
  The classical city produced the dialect this book teaches.}
\end{figure}
```

Độ rộng là một phân số của bề rộng vùng chữ in; `0.6\linewidth` cho cách trình bày nhỏ hơn, căn giữa, dùng cho tượng bán thân Homer. Chú đề luôn xuất hiện dưới hình được in.

Ghi nhận nguồn hình ở phần cuối để cuốn sách in ra tự chứng minh nguồn của chính nó. Trong `main.tex`, sau dòng `\input` cuối và trước `\PSEPrintIndex`, bản demo có:

```tex
\PSEBeginBackMatter
\chapter*{Image Credits}
\addcontentsline{toc}{chapter}{Image Credits}
The illustrations in this book come from Wikimedia Commons and are in the
public domain: the Parthenon photograph (Chapter 1), the British Museum
bust of Homer (Chapter 1), and the sixth-century Greek cursive manuscript
(Chapter 5).
\PSEPrintIndex
```

## Bước 4. Gõ tiếng Hy Lạp cổ với đầy đủ dấu

Tiếng Hy Lạp đa dấu dùng dấu hơi và dấu thanh mà các phông chính văn thông thường không luôn có. PSE giải quyết việc này bằng mô-đun ngữ nghĩa `multilingual` và một phông đủ đầy đủ cho tiếng Hy Lạp. Mở `config/semantic-modules.json` trong dự án và thêm `multilingual` vào danh sách activate:

```json
{
  "schema_version": "1.1",
  "activate": ["multilingual"],
  "deactivate": [],
  "config": {}
}
```

Sau đó bọc mỗi đoạn văn tiếng Hy Lạp trong `\PSEGreek{...}`. Trong một câu, nó trông như sau (Chương 3):

```tex
The word \PSEGreek{λόγος} (word, account) shows the endings of a whole
family of masculine nouns.
```

Và một trích dẫn trọn ở Chương 5 đọc là:

```tex
\PSEGreek{ὁ} \PSEGreek{ἄνθρωπος} \PSEGreek{ἐν} \PSEGreek{τῇ} \PSEGreek{οἰκίᾳ}
\PSEGreek{γράφει} \PSEGreek{τὸν} \PSEGreek{λόγον} \PSEGreek{τῷ} \PSEGreek{βιβλίῳ}.
```

!!! note "Phông chữ trên máy của bạn"
    Mô-đun dựa vào một họ phông đủ đầy đủ cho tiếng Hy Lạp (PSE dùng Gentium Plus theo mặc định). Đa số bản phân phối TeX có sẵn nó; nếu chữ Hy Lạp bị thiếu hoặc hiển thị sai trong PDF, xem [Cài đặt và kiểm tra PSE](install.md) để biết gói phông cần thêm, rồi chạy lại `pse build .`.

## Bước 5. Tạo lập và kiểm tra

Từ thư mục gốc dự án, chạy bộ ba chuẩn:

```text
pse build .
pse check . --human
pse inspect-output .
```

Mỗi lệnh góp phần:

- `pse build .` chạy dàn trang và ghi PDF hoạt động vào `build/book.pdf`. Lặp lại sau mỗi lần sửa; tạo lập lại luôn an toàn.
- `pse check . --human` in các phát hiện máy theo bốn cấp của PSE. Sửa hết mọi `error` trước khi tiếp tục; chú ý các mục `warning`; các mục `review` cần phán đoán biên tập của bạn. Xem [Tạo lập và kiểm tra PDF](build-and-check.md) để biết cách đọc báo cáo.
- `pse inspect-output .` ghi lại đường cơ sở soát PDF hoàn thành (siêu dữ liệu, điều hướng, khả năng trích xuất văn bản).

Mở `build/book.pdf` và nhìn vào nó. Kiểm tra máy không thể quyết mọi câu hỏi thiết kế chữ; mắt bạn là một phần của vòng lặp hoàn thành.

## Bước 6. Những gì thấy trong PDF hoàn thành

- mục lục liệt kê năm chương và xuất hiện ở phần đầu;
- Chương 1 có ảnh Parthenon với chú đề, và tượng bán thân Homer;
- Chương 5 có trang bản thảo thế kỷ thứ sáu;
- các từ Hy Lạp như ἄνθρωπος được in với dấu hơi nguyên vẹn;
- chỉ mục phía cuối tập hợp các thuật ngữ then chốt được đánh dấu bằng `\PSEIndex{...}` trong các chương.

## Nếu có gì đó sai

- **`LuaLaTeX is not available on PATH.`** Máy của bạn chưa cài bản phân phối TeX. Làm theo [Cài đặt và kiểm tra PSE](install.md), rồi xác nhận bằng `pse doctor`.
- **Một thông báo tạo lập nêu tên tệp dưới `assets/`.** Kiểm tra rằng hình tồn tại trong thư mục `assets` của dự án và tên tệp khớp đúng dòng `\includegraphics`.
- **Văn Hy Lạp in không có dấu thanh.** Kiểm tra Bước 4: mô-đun `multilingual` phải có trong `config/semantic-modules.json`.
- Vấn đề khác: [Xử lý sự cố lần đầu](troubleshooting.md).

Hoàn thành? Tiếp tục với [Bước tiếp theo](next-steps.md).
