import os
from fastapi import FastAPI, APIRouter, UploadFile
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from PIL import Image
import io
from fastapi.responses import StreamingResponse

from app.images import router as image_router
from app.core.main_router import router as main_router
from app.auth import router as auth_router
from app.users import router as users_router
from app.pinpoints import router as pinpoints_router
from app.core.logger import init_logging
from fastapi.middleware.cors import CORSMiddleware


from app.images.model import ForestSegmentation
import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
import io
import time


load_dotenv(".env")

root_router = APIRouter()

model = ForestSegmentation(
    encoder_channel=[16, 32, 64, 128],
    decoder_channel=[128, 64, 32, 16],
    input_channels=3,
    bottom_channels=256,
    class_number=2,
)

# Load model weights (adjust path as necessary)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
best_weight = torch.load(
    "./rgb_forest_segmentation_model_0.9076792001724243_iou.pt", map_location=DEVICE
)
model.load_state_dict(best_weight)
model.eval()


def process_image(image):
    # Check if the image is not in 'RGB' mode
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Define the transformation: resize to 512x512 and convert to tensor
    transform = transforms.Compose(
        [
            transforms.Resize((512, 512)),  # Resize the image to 512x512
            transforms.ToTensor(),  # Convert the image to a PyTorch tensor
        ]
    )

    # Apply the transformation
    tensor_image = transform(image)

    # Now tensor_image is a PyTorch tensor ready to be used in your model

    with torch.no_grad():
        # Predict
        prediction = model(tensor_image.unsqueeze(0))

        print(prediction.shape)

        predicted_mask = torch.argmax(prediction[0], axis=0)

        print(predicted_mask.shape)

        print(type(predicted_mask))

    if predicted_mask.dtype != torch.float32:
        predicted_mask = predicted_mask.float()  # Convert tensor to float

    model_output = predicted_mask.unsqueeze(0)  # Shape becomes [1, 512, 512]

    # Make sure your tensor is on CPU and has the right type
    tensor = model_output.cpu()

    # Since tensor is 0s and 1s, we directly multiply by 255 to match uint8 image range
    tensor = tensor.mul(255).byte()

    # Convert tensor to a PIL image
    # The tensor should be squeezed to remove the channel dimension if it's singular
    image = Image.fromarray(tensor.squeeze(0).numpy())

    buffer = io.BytesIO()
    # Save the image
    image.save(buffer, format="PNG")

    return buffer


app = FastAPI(title="osapiens API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins, or specify domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/images/mask", status_code=200)
async def get_mask(file: UploadFile):
    """
    gets an image.

    Returns:
        mask: of the same size of as the image.
    """
    start_time = time.time()
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    buffer = process_image(image)

    buffer.seek(0)

    end_time = time.time()

    # return {"time": end_time - start_time}

    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=mask.png"},
    )


app.include_router(image_router)
app.include_router(main_router)
app.include_router(root_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(pinpoints_router)

init_logging()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
