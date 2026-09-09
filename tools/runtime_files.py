RUNTIME_MAP = [
('web/index.html','index.html'),('styles.css','styles.css'),('app.js','app.js'),('cloud-sync.css','cloud-sync.css'),('cloud-sync.js','cloud-sync.js'),('ui-current.css','ui-current.css'),('ui-current.js','ui-current.js'),('sw.js','sw.js'),('manifest.webmanifest','manifest.webmanifest'),('icon.svg','icon.svg'),
('app.bundle.part0.b64','app.bundle.part0.b64'),('app.bundle.part1.b64','app.bundle.part1.b64'),('app.bundle.part2.b64','app.bundle.part2.b64'),
('data/catalog.part0.b64','data/catalog.part0.b64'),('data/catalog.part1.b64','data/catalog.part1.b64'),('data/catalog.part2.b64','data/catalog.part2.b64'),('data/catalog.part3.b64','data/catalog.part3.b64'),('data/catalog.part4.b64','data/catalog.part4.b64'),('data/reference-renders-v10.js','data/reference-renders-v10.js'),('data/reference-renders-tx-v10.1.js','data/reference-renders-tx-v10.1.js'),
('assets/paper-kraft-card-v13.svg','assets/paper-kraft-card-v13.svg'),('assets/paper-kraft-strip-v13.svg','assets/paper-kraft-strip-v13.svg'),('assets/paper-white-card-v13.svg','assets/paper-white-card-v13.svg'),('assets/paper-notebook-card-v13.svg','assets/paper-notebook-card-v13.svg'),('assets/paper-yellow-card-v13.svg','assets/paper-yellow-card-v13.svg'),('assets/paper-crumple-overlay-v13.svg','assets/paper-crumple-overlay-v13.svg')]
RUNTIME_MAP.append(('assets/camera-art.svg','assets/camera-art.svg'))
RUNTIME_MAP.append(('assets/road-plate.svg','assets/road-plate.svg'))
RUNTIME_MAP.append(('assets/collection-art.svg','assets/collection-art.svg'))
RUNTIME_MAP.extend([('assets/atlas-art.svg','assets/atlas-art.svg'),('docs/OSWALD-LICENSE.txt','OSWALD-LICENSE.txt')])
RUNTIME_MAP.append(('photo-editor.js','photo-editor.js'))
RUNTIME_MAP.extend([('trip-features.js','trip-features.js'),('trip-features.css','trip-features.css')])
RUNTIME_FILES=[src for src,_ in RUNTIME_MAP]
