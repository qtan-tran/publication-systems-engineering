---
title: Danh sách kiểm tra phát hành
description: Dùng một danh sách kiểm tra của con người gọn trước và ngay sau khi tạo một bản phát hành ấn phẩm.
---

# Danh sách kiểm tra phát hành

Hãy dùng trang này như một lời nhắc vận hành, không phải vật thay thế cho các thủ tục biên tập, pháp lý hay tiếp cận của tổ chức bạn.

## Trước khi phát hành

- Nguồn bản thảo chuẩn chứa mọi sửa đổi đã được duyệt.
- Siêu dữ liệu ấn phẩm, dữ liệu người đóng góp, định danh, vật liệu thư mục/chỉ mục và tài nguyên đã được soát xét khi áp dụng.
- `pse build .` thành công.
- `pse check . --human` không còn phát hiện `error` chưa xử lý.
- Các phát hiện `warning` và `review` đã được người chịu trách nhiệm điều tra.
- PDF làm việc đã được soát thị giác và biên tập.
- Ngôn ngữ của sản phẩm và các thuộc tính PDF kỳ vọng khác đã được soát ở nơi liên quan.
- Quyền, riêng tư, quyền phép và các phê duyệt xuất bản đặc thù tổ chức đã được xử lý ngoài PSE ở nơi cần.

## Tạo và kiểm chứng

```text
pse release .
pse verify-release release/<release-id>
```

Nếu còn các phát hiện đọc soát đã được chấp nhận, chỉ dùng `--acknowledge-review` sau khi việc đọc soát ấy thực sự đã diễn ra.

## Sau phát hành

- Bảo toàn toàn bộ thư mục phát hành, không chỉ PDF.
- Phân phối/lưu gửi sản phẩm phát hành dành cho xuất bản, không phải `build/book.pdf` hay một bản đọc soát cho người nhận.
- Nếu cần bằng chứng kiểm toán độc lập, hãy tạo nó ngoài thư mục phát hành.
- Đừng chỉnh các tệp bằng chứng tại chỗ sau khi xuất bản; với sửa đổi, hãy tạo một bản phát hành mới từ nguồn chuẩn.
