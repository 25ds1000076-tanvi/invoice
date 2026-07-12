import base64
import requests

# Point this at your server: "http://localhost:8000" while testing locally,
# or your deployed URL (e.g. "https://your-app.onrender.com") once deployed.
BASE_URL = "http://localhost:8000"

# Path to any sample image you want to test with
# (e.g. one you extract from the sample_images described in the sample json,
# or any bar chart / receipt / table screenshot you save locally as a PNG)
IMAGE_PATH = "sample_receipt.png"
QUESTION = "What is the grand total on the receipt?"


def main():
    with open(IMAGE_PATH, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    resp = requests.post(
        f"{BASE_URL}/answer-image",
        json={"image_base64": img_b64, "question": QUESTION},
    )

    print("Status code:", resp.status_code)
    print("Response JSON:", resp.json())


if __name__ == "__main__":
    main()
