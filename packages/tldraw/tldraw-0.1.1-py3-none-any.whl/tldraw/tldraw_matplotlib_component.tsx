import * as React from "react";
import { TDAssetType, TDShapeType, Tldraw, TldrawApp } from "@tldraw/tldraw";

export default function App({ image_width, image_height, base64img }) {

    const [app, setApp] = React.useState()

     const handleMount = React.useCallback((app: Tldraw) => {
         setApp(app)
     }, []);

     React.useEffect(() => {
         if (app) {
          app.patchAssets({
            myAssetId: {
              id: "myAssetId",
              type: TDAssetType.Image,
              size: [image_width, image_height],
              fileName: "card-repo.png",
              src: base64img,
            },
          });
      
          app.createShapes({
            id: "myImage",
            type: TDShapeType.Image,
            assetId: "myAssetId",
            point: [0, 60],
            size: [image_width, image_height],
            isLocked: true,
          });
      
         }
     }, [base64img, app])




  return (
    <div
      style={{
        position: "relative",
        width: image_width,
        height: image_height + 120,
      }}
    >
      <Tldraw onMount={handleMount} showMenu={false} showPages = {false} />
    </div>
  );
}
