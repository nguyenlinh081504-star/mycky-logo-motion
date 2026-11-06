# Những bài học đã có từ các dự án Mycky

Nguồn: yêu cầu/sửa đổi trực tiếp trong chat và brief/source/QA local đã đọc. Đây
là case-specific constraints, không áp tất cả lên logo mới. Brief V12/V14… có
thể là prototype raster; không gọi là vector đã nghiệm thu chỉ vì có QA JSON.

| Case | Bài học có thể tái dùng | Điều không được suy rộng |
|---|---|---|
| VENUS NAIL V12 | V/N vào lớn; N exit riêng; V giữ identity thành swash + trụ phải; serif trái top-down; vòng liên tục; sao ngay sau vòng, trước group shrink; tên sau thu | sao không mặc định cuối mọi phim; không học N→icon từ AI reference |
| THE PHIA | một bút qua 9 cubic; arc-length đều; hai trụ có thứ tự top-down sau nét chính; chưa tới bút không hiện; sao theo icon khi thu | không dùng mask rộng để lộ trước vòng ở giao điểm |
| OHANA V10 | H gồm L/R/bridge, junction chung; L thành móc dưới, R thành cung trên; bridge vẫn nối; O có outer/inner cùng morph | không lấy target có lẫn vòng O thay H; không ép độ dày cung trên quá lớn |
| NAIL ART THEORY V12 | NA giữ scale khi reposition; rút diagonal N và làm mảnh crossbar A riêng; khung xong mới vẽ swash A→N; sao rồi group shrink | không squash toàn chữ khi chỉ yêu cầu tịnh tiến; không cắt trắng chữ nhật |
| GX STUDIO V17 + sửa user | styled G giữ; clone trùng đủ nét rồi mới rút nét; original angle=0; chỉ clone flip Y một lần 0→180; chữ tên hiện cả cụm theo sửa mới | không xoay cả hai, không mặc định mọi duplicate phải xóa nét ngay; rigid mirror có thể không fit 100% target |
| PHONG LAN V14 | P riêng phải có đầy đủ chân cong trước ghép L; L chỉ trục; ghép chỉ translate; cung thêm phải bắt đầu từ trục L đúng hướng | không vẽ lại chân P sau ghép; không cho arc/star lộ trước |
| CARINR V19 + sửa user | R stem được fade đồng thời bowl+leg morph vì user yêu cầu rõ; tăng tốc đúng đoạn biến, không toàn phim nếu chưa yêu cầu; sửa geometry trước nhịp | ngoại lệ fade stem không cho phép fade toàn morph khác |
| LUMI V14 + sửa user | L source đúng ảnh, từ phải; căn ink bbox và nâng entry/morph theo user; giữ module gốc; chỉ clone xoay; sao sau khớp | không căn theo canvas PNG/baseline logo; không tự tạo block L gần giống |
| BÍCH BELLA V22/biến thể | B thường nhỏ hơn; thu nét có anatomy và 2 khoảng âm; morph hoàn tất, hold, căn góc/scale/vị trí, hold rồi mới clone quanh tâm | không vừa morph vừa xoay, không phân mảnh chữ B tùy tiện |
| BLING BLING V19 | B→ribbon/đuôi cần bù visible geometry velocity; easing bậc cao có thể làm cảm giác chậm; tail phải mọc từ thân; subpixel coverage khác crossfade | không nhận 10-microsecond metric là frame nguồn; không kết luận 60fps là mượt; có răng cưa phải xem trace/coverage |
| JIA V24–V26 | p=0 và p=0+ cùng raster; counter B ghép semantic góc thân/bowl, không global min(x,y); cleanup chỉ bridges; bảo toàn đáy B qua shrink; reparameterize visible union | số khoang/component PASS chưa chứng minh hình đẹp: user vẫn thấy nét rối khi counter corner bị kéo sai |
| Xuất 2×/2,1× | phân biệt speed và supersampling; giữ cuối lấy frame hoàn thiện thực, thay hold cũ nếu user muốn đúng 1s; H264 High/yuv420p/faststart | không âm thầm kéo duration trở lại 8s; không thêm hold nếu user chỉ yêu cầu tăng tốc |

## Chẩn đoán nhanh từ triệu chứng

- **Nhảy lúc morph bắt đầu rồi đứng:** source mask và path renderer không cùng
  endpoint/coverage hoặc resample làm mất vertex. So frame trước/sau boundary.
- **Góc nhọn mọc trong bụng chữ:** anchor counter sai semantic hoặc winding; sửa
  cặp góc và arc section. Không chỉ thêm điểm/easing toàn contour.
- **Mảng đen ở giao:** ownership/overlap/width, topology; kiểm tách màu debug nội bộ.
- **Nét đứt:** shared junction không được ràng buộc hoặc cleanup ăn vào official.
- **Nét biến mất rồi quay lại cuối:** target registration đổi trong shrink hoặc
  mask tách icon-wordmark cắt chân chữ, không phải lỗi encoding đơn thuần.
- **Xoay lắc/khựng:** sai pivot, nhiều tween cùng property, angle wrap 180→-180,
  interpolation quaternion/axis không đúng; dùng góc unwrapped và owner duy nhất.
- **Vẫn chậm dù giảm duration:** easing khiến đầu morph gần như bất động hoặc
  phần point travel bị che bởi overlap; đo visible union, không chỉ số điểm.
- **Tải về không xem được:** kiểm probe/decode trước; H264 High444/qp0/codec lạ
  không giống bản H264 High yuv420p thông dụng; không chỉ đổi đuôi filename.
- **Preview trắng/connection refused:** xác nhận server managed còn chạy và URL
  HTTP200. Không mở tab chết rồi nói đã mở. Không cài lại Motion Canvas vô cớ.
