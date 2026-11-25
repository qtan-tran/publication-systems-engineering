---
title: Hệ thống định vị và tra cứu
description: Định vị chuẩn, điểm neo, mục lục, chỉ mục và các mối quan hệ tham chiếu giúp người đọc tìm lại chính xác một nội dung.
---

# Hệ thống định vị và tra cứu

Một cuốn sách học thuật không chỉ là một chuỗi trang được đọc theo thứ tự. Nó còn là một mạng lưới những mối quan hệ cho phép người đọc chuyển từ một ý tưởng, khái niệm hoặc chú thích đến vị trí có liên quan. Một hệ thống định vị tốt phải cho phép người đọc tìm lại chính xác một nội dung, ngay cả khi hình thức cuốn sách thay đổi.

## Định danh, điểm neo và dấu chỉ

| Thuật ngữ | Giải thích |
| --- | --- |
| **Định vị văn bản** (locator) | Một thông tin dùng để xác định vị trí của nội dung, chẳng hạn số trang, số chương, số dòng thơ hoặc mã đoạn văn. |
| **Định vị chuẩn** (canonical locator) | Định danh theo một quy ước tham chiếu được xác lập cho tác phẩm hoặc ấn bản nguồn. Nó không thay đổi chỉ vì sách được dàn lại hoặc in ở khổ khác. |
| **Hệ định vị** (locator scheme) | Tập hợp các quy tắc xác định cách đánh số, tổ chức và tham chiếu các đơn vị của một văn bản. |
| **Tập định vị** (locator set) | Tập hợp tất cả các định vị được kỳ vọng hoặc thực tế có trong một văn bản. Việc so sánh hai tập hợp giúp phát hiện những vị trí thiếu, thừa hoặc sai. |
| **Điểm neo** (anchor) | Một địa chỉ được đặt tại một vị trí xác định bên trong tài liệu điện tử. Liên kết có thể sử dụng địa chỉ này để đưa người đọc đến đúng đoạn nội dung. Điểm neo thường không nhìn thấy được. |
| **Dấu chỉ vị trí** (marker) | Ký hiệu hiển thị giúp người đọc nhận biết vị trí của mình trong văn bản, chẳng hạn các số dòng in ngoài lề của *Nữ Bái Thần*. |
| **Đích tham chiếu** (destination) | Vị trí mà một liên kết hoặc thao tác tra cứu đưa người đọc đến. |
| **Điểm neo trùng** (duplicate anchor) | Hai hoặc nhiều vị trí khác nhau sử dụng cùng một định danh điểm neo, khiến đích tham chiếu có thể trở nên không xác định hoặc sai lệch. |
| **Điểm neo thiếu** (missing anchor) | Một địa chỉ đáng lẽ phải tồn tại nhưng không được tạo ra, khiến một phần nội dung không thể được truy cập đúng qua hệ thống tham chiếu. |
| **Số trang hiển thị** (folio) | Số trang được in trên trang sách, thường xuất hiện ở đầu hoặc cuối trang. Số này không nhất thiết giống số thứ tự trang vật lý trong tệp PDF. |

### Phân biệt bốn khái niệm gần nhau

Xét một câu thơ 815 của kịch Hy Lạp: **định vị chuẩn** là con số 815 theo quy ước của ấn bản nguồn; **địa chỉ kỹ thuật** của điểm neo, ví dụ `sourceverse.815`, là địa chỉ máy đọc được; **dấu chỉ được in** là con số 815 người đọc nhìn thấy ngoài lề; **số trang** 42 thuộc về ấn bản cụ thể. Khi dàn lại sách, câu thơ 815 có thể chuyển từ trang 42 sang trang 45: định vị chuẩn vẫn là 815, nhưng vị trí thực tế của điểm neo, dấu chỉ và số trang cần được cập nhật tương ứng. Bốn khái niệm này có quan hệ chặt chẽ nhưng không đồng nhất.

## Các hệ định vị khác nhau

| Loại ấn bản | Hệ định vị có thể sử dụng | Ví dụ |
| --- | --- | --- |
| Đối thoại Plato | Hệ Stephanus | 80d |
| Tác phẩm Aristotle | Hệ Bekker | 1094a1 |
| Kịch Hy Lạp | Số câu thơ theo ấn bản nguồn | 815 |
| Kinh điển đánh số đoạn | Chương và đoạn | 3.12 |
| Sách chuyên khảo | Chương, mục, tiểu mục | 2.3.1 |
| Giáo trình | Bài học, bài tập | Bài 12, bài tập 4 |

## Kiến trúc định vị dùng chung

**Mô hình định vị chuẩn dùng chung** (canonical locator abstraction) là một nguyên tắc kiến trúc cho phép PSE quản lý nhiều hệ định vị khác nhau bằng cùng một cơ chế tổng quát, nhưng không áp đặt cùng một quy tắc đánh số cho mọi tác phẩm. Chẳng hạn, PSE có thể hiểu rằng cả `80d` của Plato và `815` của Euripides đều là định vị nguồn, nhưng hệ thống phải hiểu rằng chúng thuộc hai quy ước khác nhau.

**Bộ kiểm định theo hệ định vị** (locator-scheme validator) là cơ chế kiểm tra tính hợp lệ của định vị dựa trên quy tắc riêng của từng loại văn bản: bộ kiểm định cho Stephanus không giống bộ kiểm định cho số câu thơ, và cả hai không giống bộ kiểm định cho cấu trúc chương, mục, tiểu mục.

Đây là ví dụ về tiêu chuẩn hóa đúng nghĩa: **dùng chung nguyên tắc kiến trúc, nhưng bảo toàn đặc thù của từng văn bản**.

### Sổ đối chiếu nội dung

**Sổ đối chiếu ngữ nghĩa** (semantic alignment ledger) là một hồ sơ có cấu trúc ghi nhận quan hệ giữa từng đơn vị văn bản nguồn, bản dịch, người nói, điểm neo, vị trí trong ấn bản và kết quả kiểm chứng. Ví dụ giản lược:

| Định vị nguồn | Người nói | Đối ứng bản dịch | Trang | Kiểm định nội dung |
| --- | --- | --- | --- | --- |
| 810 | Nhân vật A | Đã xác định | 42 | Đã đối chiếu |
| 811 | Nhân vật B | Đã xác định | 42 | Cần kiểm tra |
| 812 | Nhân vật A | Đã xác định | 42 | Đã đối chiếu |
| 813 | Nhân vật A | Chưa xác nhận | 43 | Còn mở |

Bảng minh họa cho thấy một đơn vị có thể đã được định vị đầy đủ về mặt kỹ thuật nhưng chưa được xác nhận về mặt nội dung. Sổ đối chiếu không phải một bản dịch thứ hai; nó là hồ sơ chứng cứ giúp người biên tập biết từng phần của văn bản đã được xử lý đến đâu.

Trong báo cáo kỹ thuật của *Nữ Bái Thần*, mô hình định vị dùng chung, sổ đối chiếu và bộ kiểm định riêng cho từng hệ định vị được đề xuất như những cải tiến có thể tái sử dụng trong PSE, chưa phải những tính năng đã được xác nhận triển khai đầy đủ vào hệ thống lõi.

## Các thành phần của hệ thống tra cứu

| Thuật ngữ | Giải thích |
| --- | --- |
| **Mục lục** (table of contents) | Danh sách các phần của sách, thể hiện cấu trúc phân cấp và vị trí bắt đầu của chúng. |
| **Cây điều hướng** (outline) | Cấu trúc phân cấp các phần có thể được mở trong trình đọc PDF để chuyển nhanh giữa các chương và mục. |
| **Dấu trang điện tử** (bookmark) | Một mục có thể chọn trong hệ thống điều hướng của tài liệu điện tử. Trong ngữ cảnh chế bản PDF, các dấu trang thường tạo thành cây điều hướng. |
| **Liên kết** (link) | Cơ chế đưa người đọc từ một vị trí đến vị trí khác, trong cùng cuốn sách hoặc đến tài liệu bên ngoài. |
| **Tham chiếu chéo** (cross-reference) | Một chỉ dẫn từ nội dung hiện tại đến một nội dung khác có liên quan, chẳng hạn "xem chương 3" hoặc "xem chú thích câu 815". Có thể tồn tại cả trong sách in lẫn sách điện tử. |
| **Liên kết ngược** (reverse link) | Liên kết cho phép quay về vị trí xuất phát, chẳng hạn từ chú thích trở lại đoạn chính văn đang đọc. |
| **Khóa chú thích** (note key) | Định danh nội bộ của một chú thích, giúp hệ thống nhận diện chú thích đó ngay cả khi số thứ tự hiển thị thay đổi. |
| **Khóa chỉ mục** (index key) | Định danh dùng để tập hợp và sắp xếp các lần xuất hiện của một mục từ trong chỉ mục. |
| **Mục từ chỉ mục** (index entry) | Tên người, địa danh, sự kiện hoặc khái niệm được trình bày trong chỉ mục, kèm các vị trí liên quan. |
| **Mục từ phụ** (subentry) | Thành phần nằm dưới một mục từ chính, giúp phân biệt các phương diện khác nhau của cùng một chủ đề. |
| **Mục từ hiển thị** (display term) | Cách một thuật ngữ thực tế xuất hiện trước người đọc. Có thể khác với khóa nội bộ dùng để quản lý và sắp xếp. |
| **Nhãn trang điện tử** (PDF PageLabels) | Thông tin giúp trình đọc PDF hiển thị tên hoặc số trang theo quy ước của sách, chẳng hạn "Bìa", "iv" hoặc "1", thay vì chỉ đếm từ trang đầu tiên của tệp. |

## Các mối quan hệ ngữ nghĩa

**Quan hệ tham chiếu** (semantic edge) là một mối quan hệ có ý nghĩa giữa hai thành phần nội dung. Ví dụ, một chú thích về ngọn núi Cithaeron được liên kết với đoạn chính văn nói đến địa danh này. Điều cần bảo đảm không chỉ là liên kết hoạt động, mà là nó dẫn đến đúng nội dung cần giải thích.

| Thuật ngữ | Giải thích |
| --- | --- |
| **Kiểm tra liên kết kỹ thuật** | Xác minh liên kết tồn tại, hoạt động và có đích hợp lệ. |
| **Đối soát ý nghĩa liên kết** (link semantic reconciliation) | Kiểm tra xem liên kết có đưa người đọc đến đúng đối tượng cần tham chiếu về mặt nội dung hay không. |
| **So sánh quan hệ tham chiếu** (diff semantic edges) | Đối chiếu mạng lưới quan hệ giữa hai phiên bản sách để xác định liên kết nào được thêm, bỏ, thay đổi hoặc chuyển sai đích. |
| **Tính nhất quán số trang** (folio consistency) | Sự tương ứng giữa số trang được in, mục lục, chỉ mục, nhãn trang điện tử và đích của các liên kết. |
| **Đối soát mục lục và số trang** (TOC/folio consistency) | Kiểm tra xem mỗi mục trong mục lục có ghi đúng số trang và dẫn đến đúng vị trí bắt đầu của phần tương ứng hay không. |
| **Chuẩn hóa bảng thuật ngữ và chỉ mục** (glossary/index normalization) | Thống nhất cách viết, chuyển tự, sắp xếp, quản lý tên gọi thay thế và phân cấp mục từ, tránh tạo ra các mục trùng lặp hoặc không nhất quán. |

### Tại sao cần kiểm tra cả ý nghĩa lẫn kỹ thuật?

Giả sử một chú thích có liên kết đến trang 42. Khi nhấp vào, trình đọc thực sự mở trang 42: về mặt kỹ thuật, liên kết hoạt động. Tuy nhiên, sau khi hiệu đính bản dịch, nội dung cần chú giải đã chuyển sang trang 43; liên kết lúc này không còn đúng về mặt ý nghĩa.

Điều tương tự xảy ra với số lượng liên kết: việc một phiên bản mới có ít hơn năm liên kết không chứng minh rằng năm liên kết bị hỏng; có thể những liên kết trùng đã được loại bỏ hoặc cách xuống dòng đã thay đổi.

**Đối tượng cần kiểm định là quan hệ giữa các nội dung, chứ không chỉ là số lượng liên kết.**

Bảng thuật ngữ liên quan: [Cấu trúc logic của văn bản](semantic-structure.md), [Kiểm soát chất lượng và phát hành](quality-assurance.md).
