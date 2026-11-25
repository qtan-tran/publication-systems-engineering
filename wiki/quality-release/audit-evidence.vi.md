---
title: Bằng chứng kiểm toán
description: Tạo và kiểm chứng các bản ghi kiểm toán phát hành tách rời và các gói xuất chỉ chứa bằng chứng tất định mà không sửa đổi bản phát hành ấn phẩm.
---

# Bằng chứng kiểm toán

Bằng chứng kiểm toán cố tình **tách rời** khỏi bản phát hành ấn phẩm mà nó mô tả. Điều này cho phép người kiểm toán ghi lại kết quả kiểm chứng về sau mà không phải viết lại thư mục phát hành.

## Kiểm toán một bản phát hành

```text
pse audit-release /path/to/release \
  --output /path/to/audits/release-audit.json
```

Đường dẫn sản phẩm phải nằm ngoài bản phát hành được kiểm toán.

Kiểm chứng bản ghi kiểm toán tự nó:

```text
pse verify-audit-record /path/to/audits/release-audit.json --human
```

hoặc gắn lại nó vào bản phát hành khi kiểm chứng:

```text
pse verify-audit-record /path/to/audits/release-audit.json \
  --release-dir /path/to/release --human
```

## Kiểm toán một bộ sưu tập

Với một thư mục mà các thư mục con trực tiếp của nó là các bản phát hành:

```text
pse audit-index /path/to/releases \
  --output /path/to/audits/audit-index.json --human
```

Chỉ mục là bằng chứng độc lập đường dẫn trên tập phát hành được kiểm toán. Kiểm chứng nó tách rời hoặc gắn lại vào một bộ sưu tập bằng `pse verify-audit-index` với `--collection-dir`.

## Xuất bằng chứng

Tạo một ZIP tất định chỉ chứa bằng chứng kiểm toán:

```text
pse export-audit-evidence /path/to/audits/evidence.zip \
  /path/to/audits/release-audit.json \
  /path/to/audits/audit-index.json --human
```

Bản xuất không chứa PDF xuất bản. Nó không phải một chữ ký số, khẳng định PKI, dấu thời gian tin cậy, dịch vụ chứng thực hay bằng chứng rằng một kho bên ngoài đã bảo quản các tệp. Những điều đó đòi một tầng tin cậy riêng.
