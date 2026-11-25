---
title: Tạo lập sạch và khả năng tái tạo
description: Xóa trạng thái được sinh và xác nhận một dự án có thể được tạo lại từ nguồn chuẩn.
---

# Tạo lập sạch và khả năng tái tạo

Một lần tạo lập sạch hữu ích trước một bản đọc quan trọng, sau thay đổi cấu hình, sau khi đổi máy, hoặc bất cứ khi nào bạn nghi các tệp trung gian lỗi thời đang ảnh hưởng sản phẩm.

Chạy:

```text
pse clean .
pse build .
pse check . --human
```

`pse clean` xóa các các sản phẩm tạo lập được sinh trong khi giữ nguồn chuẩn và tài nguyên của người dùng. Mục đích không phải dọn dẹp hình thức; nó kiểm tra xem dự án có thể tái tạo sản phẩm làm việc của nó từ nguồn và cấu hình được khai báo hay không.

## Một lần tạo lập sạch cho biết gì

Một lần tạo lại sạch thành công cho bằng chứng rằng dự án hiện hành không phụ thuộc vào một tệp được sinh sót lại từ lần chạy trước. Nó không chứng minh hai hệ điều hành hay hai bản TeX khác nhau sẽ tạo PDF giống nhau từng byte, trừ khi các điều kiện môi trường và tạo lập tất định liên quan cũng được kiểm soát.

Trước một bản phát hành ấn phẩm, tuyến phát hành của PSE tự thực hiện một lần tạo lại ranh giới sinh sạch và áp các chốt phát hành. Bạn không cần tự biến một `build/book.pdf` làm việc thành một bản phát hành.

## Đừng dọn mất lai lịch bạn muốn giữ

Bản đọc soát cho người nhận và các bản phát hành ấn phẩm có vòng đời khác với các trung gian làm việc dùng xong bỏ. Hãy bảo quản các thư mục phát hành và mọi bằng chứng kiểm toán theo chính sách hồ sơ của tổ chức bạn, thay vì coi chúng là bộ nhớ đệm tạo lập tạm.

Tiếp: [Chuẩn bị phát hành ấn bản](publication-release.md).
