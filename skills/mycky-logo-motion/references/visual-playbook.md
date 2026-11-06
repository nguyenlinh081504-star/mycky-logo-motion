# Visual playbook v2 — từ artwork đến chuyển động có logic

Đọc bài đúng họ hình học, **mở ảnh và xem video thật**, rồi dùng code tương ứng.
Không đọc tên công thức rồi tự viết lại một phép morph toàn silhouette. Các bài
B/KJ dưới đây là hình giáo dục tự dựng, không phải logo đích hay font thay thế.
Các video thương hiệu là tham chiếu nhịp/cơ chế; artwork khách mới luôn có quyền
quyết định hình học cuối. Không cam kết mọi logo đều có cùng một đáp án.

## Xem gì trước?

| Cấu trúc logo mới | Bài chạy được | Cơ chế catalog | Bất biến cần khóa |
|---|---|---|---|
| B/P/D/O có khoang âm | [video](../assets/lessons/counter.mp4), [ảnh](../assets/lessons/counter-middle.png) | F02/F08/F31 | outer và từng counter riêng; thân/cổ không sập |
| Hai chữ lồng, nối, đan; H có bridge | [video](../assets/lessons/interweave.mp4), [ảnh](../assets/lessons/interweave-middle.png) | F11/F16/F17/F18/F32 | glyph đầy đủ bên dưới; điểm nối chung; nét đè có owner |
| Một module + một clone quay | [video](../assets/lessons/clone.mp4), [ảnh](../assets/lessons/clone-middle.png) | F21/F22/F23/F26 | source=clone; original đứng yên; pivot và trục đúng |
| Nét cong/vòng được vẽ | [video](../assets/lessons/draw.mp4), [ảnh](../assets/lessons/draw-middle.png) | F27/F28/F29 | prefix arc-length, điểm bắt đầu gắn đúng trục |
| Nhiều module lặp thật | [video](../assets/lessons/radial.mp4), [ảnh](../assets/lessons/radial-end.png) | F04/F06/F24/F25/F40 | fit tĩnh mọi module; original không quay tùy tiện |
| N/A/R có nét phải giản lược | [video](../assets/lessons/retract.mp4), [ảnh](../assets/lessons/retract-middle.png) | F09/F10/F12/F18 | chỉ nét được giao rút/mỏng/fade; trụ không co theo |
| Đặt hai chữ vào icon trước morph | [video](../assets/lessons/placement.mp4), [ảnh](../assets/lessons/placement-middle.png) | F19 + họ morph phù hợp | position có owner; scale và geometry khóa trong pha đặt |
| H với bridge và O bao quanh | [video](../assets/lessons/hbridge.mp4), [ảnh](../assets/lessons/hbridge-middle.png) | F11 + F08 | bridge lấy hai điểm thật trên thân; O giữ outer/inner |
| S thường → module → 4 bản ghép | [video](../assets/lessons/sassembly.mp4), [ảnh](../assets/lessons/sassembly-middle.png) | F06 → F25 | hoàn tất lobe/waist/terminal trước clone; không bật module đích ra |

Mở [phòng thí nghiệm SVG](visual-lessons.html): chọn bài, kéo thanh thời gian,
bật/tắt màu phân vai. `window.renderAt(t,{lesson:'interweave',debug:true})`
seek ngược/xuôi cho cùng frame; không dùng timer để tạo trạng thái hình học.
Video là render từ chính SVG/code này, không phải video dựng AI hoặc frame
TikTok nội suy giả. Chúng dạy kỹ thuật; **không coi hình giáo dục là thẩm mỹ đích**.

## 1. Chuyển phân tích thành source cụ thể

Trước animation phải có 4 hình nội bộ:

1. **Artwork nguyên bản:** icon, accent, tên đúng nguồn và tỷ lệ; PNG phải xem
   trên nền phù hợp, không thấy hình đen trên nền trong suốt rồi đoán bừa.
2. **Glyph rời hoàn chỉnh:** mỗi chữ có đủ nét bị che/dùng chung. Tách pixel
   nhìn thấy không đủ; phục dựng tối thiểu theo ảnh chữ rời nếu có. Đánh dấu phần
   suy luận. Không thay bằng font gần giống. Có thể dùng skill logo-unweave khi có.
3. **Bản đồ màu theo anatomy:** stem, arm/bowl, hook/leg/tail, counter, bridge;
   không phải chia ảnh theo ô hoặc thành 50 mảnh cho dễ nội suy.
4. **Fit tĩnh đích:** lắp các glyph/module với pivot/transform cuối, so overlay
   với artwork. Phần nhìn thấy phải khớp; chỗ bị che có reconstruction riêng.

Nếu không dựng được hình tĩnh đúng thì chưa giải quyết được animation. Đừng
chạy full render và hy vọng easing sẽ làm ra đúng hình. Thiếu glyph nguồn thì
nói rõ inference hoặc hỏi asset đúng khi việc đó làm thay đổi thiết kế.

### Thẻ vai nét — ví dụ đã điền cho bài interweave

| Vai | Nguồn → đích | Được thay đổi | Phải giữ | Vùng giao |
|---|---|---|---|---|
| K-stem | thân trái dày → thân mảnh | width top/bottom quanh tim | tim thẳng, đầu/đáy khóa | cùng chữ K được union |
| K-arm | diagonal trên → arm mềm | hai biên cubic và tangent | gắn đúng nút stem | không mọc ra từ J |
| K-leg | diagonal dưới → ribbon | curve, taper có đích | đầu nối stem, chân ribbon | owner nét đè |
| J-hook | trụ + móc → hook kéo dài | biên móc, độ dày trụ | glyph J đầy đủ, thân không gợn | mask bởi K-leg + khe đan |

Tọa độ ví dụ cụ thể nằm trong `scripts/lesson-core.js`, `geometry.kj`.
Không lấy nguyên tọa độ này gắn cho KANJO hay logo khác. Đo source/target mới,
giữ lại **cấu trúc thuật toán**. SVG debug cho thấy trụ khóa; khe trắng được
tính cùng frame với ribbon, không được thêm vào sau khi morph xấu đã chạy qua.

## 2. Map landmark: nghĩa trước, số điểm sau

Mỗi section phải có: tên anatomy, hai endpoint source/target, corner/smooth,
tangent, profile dày–mỏng, đối tác junction và phase owner. Đi theo thứ tự:

1. Khóa tim và các mốc cấu trúc. Trụ thẳng ở cả hai đầu thì nội suy width/taper
   quanh tim, không cho control point chạy tự do ngang thân.
2. Các cung được nhận diện bằng điểm đầu/cuối/eo/cực trị; đặt handle theo tiếp
   tuyến thật. Mốc thẳng chuyển thành serif phải có quá trình phát triển từ đầu
   trụ, không là đỉnh nhọn kéo từ một điểm bất kỳ trên contour.
3. Chia theo mốc tương ứng, rồi mới resample arc-length trong section. Đủ điểm
   không sửa được mapping sai. Nếu phải đổi topology, thiết kế biến đổi cục bộ
   có owner/phase; không xem mọi outline là một vòng cùng số điểm.
4. Dùng cùng lệnh M/C/Z và cùng renderer từ q=0 đến q=1. Không mask raster ở
   đầu rồi thay path giữa chừng; không target swap ở 95%.
5. Render q=0,.1,…,1 để nhìn đường đi. Điểm chạy liên tục nhưng nét phình/gợn
   bất hợp lý vẫn fail. Sửa handle, mốc hoặc cách chia role trước khi sửa easing.

`interpolate()` trong lesson core chỉ nội suy geometry **đã được map đúng**.
Nó không nhận bitmap bất kỳ rồi tự hiểu glyph. `contractStem()` chỉ hợp cho trụ
thẳng/taper; không ép nó lên đoạn thư pháp cong thật của logo mới.
Không có họ nào phù hợp thì thiết kế role mapping mới từ artwork và kiểm đoạn
khó; không ép logo đó vào 42 công thức hoặc về một glyph mẫu.

## 3. Phương pháp cho từng họ, không học thuộc một chữ

### Khoang âm / bowl

Xem `counter.mp4`, màu viền phân biệt outer, counter trên/dưới. Ghép góc trong
thân với góc trong thân; eo với eo. Giữ cavity bằng compound path. Trong SVG
dùng evenodd, hoặc winding đúng nếu engine dùng nonzero. Không vẽ hình trắng
đè lên để giả hole vì sẽ sai nền/overlap/alpha. Không normalize counter độc lập
theo bbox riêng làm hai lỗ trượt khỏi thân.

### Đan chữ / junction

Xem `interweave.mp4`. Một chữ có thể bị che nhưng geometry đầy đủ vẫn phải liền.
Xác định nét nào ở trên và ở dưới cho **từng crossing**, không áp một mask toàn
icon. Mask giao cần đi theo nét owner hiện tại và độ rộng khe thật. Không cộng
alpha hai thân gây đậm kép; không dùng cleanup muộn để làm giữa phim thành cục
đen. H/bridge lấy endpoint từ hai thân đang morph, không tween rời ba thành phần.
Bài `hbridge.mp4` chạy chính cách này: `hState(q)` lấy điểm trên cubic trái/phải
bằng `cubicAt()`, rồi dựng bridge nối hai điểm hiện tại. Điểm debug theo thân
suốt tiến trình; không dùng đường lý tưởng độc lập để chứng minh render không
đứt. Kiểm trụ cũng phải sample từ chính cubic đang render.

### Module / clone / radial

Xem `clone.mp4` và `radial.mp4`; đối chiếu Sắc Son. Module hoàn thiện → hold →
căn góc nếu brief có → clone trùng → clone tới góc đích. Curve module không đổi
trong pha xoay. Góc unwrapped đơn điệu và một property owner. Kiểm 90° nếu flip
Y, 180° nếu half-turn Z. Bài clone là rotation Z, **không phải flip Y**. Số module,
trục, chiều và thứ tự phải lấy từ artwork/quan sát mới; không áp k=4 cho mọi logo.

`sassembly.mp4` có toàn chuỗi source S → module → hold → lắp, không chỉ đầu
vào là module đã xong. Các cubic upper lobe/waist/lower terminal ở
`sModulePath(q)` khớp đúng `modulePath` tại q=1; clone dùng lại path đó. Đây là
ví dụ stroke đều để thấy mapping; khách có dày–mỏng cần hai biên/filled outline.
`radialState(t,k)` hỗ trợ k khác 4 nhưng phải đặt duration ≥ `radialDuration(k)`;
laboratory sáu giây chỉ minh họa k=4, không coi sáu giây là đủ cho mọi k.

### Giản lược / draw-on

Xem `retract.mp4`: chỉ thanh phụ được rút hoặc mỏng quanh tim. Không bóp trụ để
giấu thanh. Fade chỉ hợp khi user/concept cho phép rõ, không phải giải pháp cho
morph không map được. Xem `draw.mp4`: tách prefix bằng arc-length và de Casteljau.
Nét thư pháp cần reveal trong miền bút, không lộ toàn silhouette ở các crossing.

### Placement / lockup

Xem `placement.mp4`: pha position không tự đổi scale/shape. Sau khi morph/lắp
đạt, icon + accent cùng một parent để shrink; giữ relative transform. Wordmark
dùng artwork gốc. Tránh crop cắt chân dài rồi “mọc lại” khi tới bố cục cuối.

## 4. Nhịp giống mẫu: đo các sự kiện, không sao chép độ méo

Trong `assets/lessons/references/` có video local mà user đã dùng tham chiếu:

- **Sắc Son:** morph S riêng → giữ module → lần lượt xoay/lắp → accent → thu → tên.
  Dùng làm chuẩn về quan hệ module/clone và nhịp. Không mượn silhouette S cho B/K.
- **Yến Chi:** hai chữ đi vào/đặt → nắn nét → lockup. So giai đoạn dày–mỏng và
  cảm giác chuyển sang serif. Đây là tài liệu quan sát, không chứng minh original
  control points hoặc source vector.

Đọc ledger `references/reference-video-ledger.json` để biết file, timecode và
giới hạn. Ảnh contact chỉ để tìm đoạn; phải phát đoạn tương ứng 1×/0,25×. Với
mẫu chuyển rất nhanh, đừng kéo giãn toàn contour ba giây thành cao su. Đo thời
gian entry/read hold/morph/module hold/assembly. Khi user muốn mềm nhưng gọn,
cắt thời gian chờ trước, chọn velocity ramp có plateau vận tốc hợp lý, không
đẩy toàn biến dạng vào 10% giữa clip. Geometry sạch mới rút duration.

## 5. Nghiệm thu khiến bản KANJO lỗi phải bị chặn

`KANJO_V1_TRIAL.mp4` là ca fail nội bộ, không phải video mẫu đạt. Qua frame:

- Khoảng 1,75–2,25s, chân K và móc J dính thành chân đen rộng.
- 2,50–3,75s, các trụ trở thành gợn, mấu và khối dày không có logic theo anatomy.
- 3,00–4,00s, crossing và negative space biến thiên hỗn độn.
- Hình đích sạch dần ở cuối không hợp thức hóa phần giữa. Không thể kết luận
  thuật toán nào đã gây lỗi nếu chưa đọc source của bản trial.

Áp dụng cho **mọi logo mới**, bằng ROI/anatomy riêng chứ không bằng tọa độ KANJO:

| Cổng | Bằng chứng phải xem | Fail thì sửa |
|---|---|---|
| Hình tĩnh | source / glyph rời / target overlay | tách vai, phục dựng, registration |
| Trụ và tangent | ROI đoạn bảo vệ ở q=.25,.5,.75 | constraint tim/handle/width |
| Khoang âm | từng cavity qua toàn tiến trình | anchors theo nghĩa, fill rule |
| Crossing | debug màu và hình thật cùng frame | ownership + gap + bridge endpoint |
| Chuyển pha | frame sát trước/sau và seek ngược | một renderer, một timeline owner |
| Cảm giác | clip khó 1× và 0,25× | time warp sau khi geometry đạt |
| File cuối | giải mã video, xem toàn timeline | codec/frame count rồi thẩm mỹ |

Không thay thế các cổng bằng `FPS=60`, hash đúng, IoU cao hoặc JSON tự ghi PASS.
Chỉ trích frame đẹp đầu/cuối là chưa kiểm morph. Các ảnh/video hướng dẫn cũng
không bảo đảm agent sau tự làm đúng; bắt buộc thực hiện kiểm trên artwork mới.

## 6. Từ ví dụ sang dự án thật

1. Mở bài thuộc họ phù hợp, xem đúng cửa sổ và code.
2. Tạo role table và `motion-contract` đã điền bằng asset mới; không giao blank.
3. Dựng skeleton + envelope, map source/target từng role, fit static trước.
4. Adapter engine: dùng `examples/counter-motion-canvas.tsx` làm mẫu nối progress
   tới native Path. Nhập geometry mới; không lấy code demo thay logo.
5. Render đoạn khó; tạo contact có timecode, debug màu, ROI và playback.
6. Ghi lỗi tìm được + file/điểm đã sửa. Chỉ sau nghiệm thu mới full render.

Kiểm code giáo dục: `node scripts/test-visual-lessons.cjs`.
Tái tạo media: `node scripts/render-lessons.cjs --playwright-module <module đã có>
--browser-executable <Chrome/Chromium đã có> --ffmpeg <ffmpeg đã có> --out <D:/job>`.
Không tải trình duyệt/framework mới khi runtime hiện có vẫn hoạt động.
