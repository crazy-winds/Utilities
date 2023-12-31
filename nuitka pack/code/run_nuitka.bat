% 将第三方库编译打包，速度极慢 %
% python -m nuitka --standalone --show-progress --show-memory --enable-plugin=matplotlib,tk-inter --output-dir=compile_party inference.py %

% 不编译第三方库，在打包完后需手动复制，可以快速完成打包 %
% --nofollow-import-to=torch,numpy,albumentations,PIL  --nofollow-imports  %
python -m nuitka --standalone  --show-progress --show-memory  --nofollow-import-to=torch,numpy,albumentations,PIL --follow-import-to=utils  --enable-plugin=matplotlib,tk-inter --output-dir=no_compile_party inference.py