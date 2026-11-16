# Hợp đồng hình học từng nét cho animation logo

## 1. Khóa các hệ tọa độ

Phân biệt ảnh nguồn kích thước W×H, ink bounding box, hệ tọa độ local của glyph, world canvas và target artwork. Đăng ký:
P_world = center + s R(theta) (P_local - pivot) + translation, s đồng nhất nếu người dùng khóa form.
Không coi center của ảnh PNG có khoảng trắng là center của nét. Lấy ink bbox, hoặc sử dụng weighted center có giải thích. Giữ transform chain nhất quán.

## 2. Semantic strand ownership

Tạo bảng mỗi nét:
- id, nguồn glyph+section, đích icon+section, landmark cặp, start/end, width profile, direction;
- giữ số counter; điểm junction ràng buộc; lớp trước/sau ở crossing; transition được phép đổi topology;
- trạng thái nhìn thấy; owner của x/y/rotation/scale/path trong mỗi pha.

Các section không được ghép theo min(x,y) hoặc sampling nguyên contour nếu những điểm đó không cùng nghĩa: bowl trên B phải map bowl trên, chân M phải map chân M; nét nối tạm có owner khác nét chính.

## 3. Nội suy cubic và width

Cubic:
B(s)=(1-s)^3 P0 + 3(1-s)^2 s P1 + 3(1-s)s² P2 + s³ P3.

Với section đã match: chia source và target tại cùng landmark; resample theo arc-length trong section. Tuyệt đối không lấy cùng index pixel toàn hình làm correspondence. Trụ cần thẳng ở cả 2 đầu phải khóa tim (x hoặc y), chỉ đổi độ dày và vị trí đúng hướng.

Đường tim C(s,t), pháp tuyến N(s,t), width w(s,t):
left=C-wN/2, right=C+wN/2.
Width chỉ gần 0 ở đầu taper có chủ ý. Ở cung gắt, offset có thể tự giao; cần sửa tim/handle/width chứ không che bằng trắng.

C1 continuity ở smooth junction: tangent của hai segment cuối/đầu phải đồng tuyến cùng hướng. C0 là bắt buộc ở điểm nối liền; C1 không bắt buộc tại góc sắc có chủ ý.

## 4. Morph nhiều giai đoạn

Chia microposes dựa chứng cứ: 0% còn nhận diện glyph → 25% đổi vị trí/bán kính → 50% phát triển nét khó → 75% gần đạt cấu trúc → 100% chuẩn artwork. Đây là nhịp dựng lại, không tự gọi là keyframe gốc khi chỉ có video mẫu.

Khi source/target không đồng topology, không thể duy trì song ánh contour trên mọi trạng thái. Chia chủ ý: interval sinh/rút nét, bridge owner, clip reveal theo path, hoặc thay đổi topology cục bộ với disclosure và QA. Không viện "perfect morph" để chèn ảnh khác.

## 5. Đặt/cắt đúng điểm nối

Điểm nối 2 nhánh phải lấy trên hai path hiện tại: J_L(q)=B_L(s_L,q), J_R(q)=B_R(s_R,q). Bridge là đoạn hoặc cubic kết nối J_L(q)→J_R(q) tại **cùng q**. Không tween endpoint theo thế giới độc lập, gây đứt nét.

Một layer over/under tại crossing, compound path fill rule nhất quán; tránh additive alpha đậm kép, tránh mask trắng phủ toàn silhouette. Cầu tạm chỉ được rút khi phase quy định, bảo toàn nét chính.

## 6. Vẽ nét theo độ dài bút

Arc-length L(u)=∫||B'(v)||dv; xây LUT nhiều điểm theo sai số ở độ phân giải đích. Với progress q∈[0,1], tìm u sao cho L(u)=q L_total, dùng de Casteljau split tại u để dựng prefix cubic thực. Chưa tới bút không được lộ nét, kể cả chỗ path tự giao. Taper/cap phải thuộc silhouette đích và được tái tạo trong miền reveal.

Nhiều nét đồng thời: cùng time progress nếu clip chứng minh đồng bộ; không giả tất cả đều vẽ nối tiếp. Ví dụ thanh nối GB mọc giữa: xL=c-Lleft q, xR=c+Lright q, khác draw-on từ trái sang phải.

## 7. Xoay và module

Rcw(theta)=[[cos,-sin],[sin,cos]] trên màn hình x phải y xuống => theta dương nhìn xoay thuận kim đồng hồ. P'=pivot+Rcw(theta)(P-pivot).

Clone từ cha đã dừng: pose clone lúc sinh = pose cha hoàn thiện; quay +90° (hoặc góc đo) trên pivot chung, không spawn trên đích. **Không nhân bản nếu target không chứng minh module lặp**. Đối với F béo trước xoay, giữ full shape và width qua toàn pha quay; chỉ morph ornament sau khi clone hoàn tất nếu brief chốt vậy.

Với X có hai thanh chéo giảm từ ±60° về ±15°, phải điều khiển từng nhánh quanh junction chung — quay whole X không làm đổi góc tương đối.

## 8. Nhịp theo cảm nhận nét

u=clamp((t-t0)/(t1-t0),0,1)
smootherstep=6u^5-15u^4+10u^3 dùng cho move/settle, không mặc định cho mọi morph. Nếu toàn chuyển động dồn giữa và nhìn như "nháy": tăng duration hoặc dùng motion_progress có ramp 15–20% và giữa gần đều; cần đo optical coverage/visible union change và reparam q bằng tích phân độ dài metric. Sửa geometry sai trước, time warp sau; không blur chữa popping.

## 9. Test được + không test được

Có thể kiểm numerically: source/target coverage, counter count/area, min-width, angle, pivot distance, endpoint, C0/C1, frame count, playback metadata, final registered silhouette.

Không thể từ một bảng PASS suy ra toàn animation đẹp, không có lỗi đọc hình hay giống video 100%. Phải xem clip 1×/0.25×, phóng ROI và so vector contours. Nêu rõ chưa kiểm nếu thiếu source hoặc chưa render.

## 10. Các lớp lỗi để chẩn đoán

- q=0 nháy: renderer/fill-rule/split source khác nhau; sửa coverage trước.
- S/bowl "nháy một phát": duration/velocity geometry dồn vào giữa; kiểm metric và microposes.
- Đáy B bị đứt/đen: mapping counter/lower bowl, ownership và cleanup cắt lấn; không xóa bừa.
- F giữ form nhưng xoay lộn: góc unwrap/pivot/shared parent ownership, không thêm translation.
- Chữ đầu dừng lệch: ink bbox so canvas PNG.
- Giao nét bệt: union/layer/width sai, không giấu bằng fade.
- Đuôi không có nguồn: ancestry/spline endpoint sai.
