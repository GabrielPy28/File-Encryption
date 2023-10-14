# File-Encryption

## First steps
* Clone the repository
* It is required to have Microsoft Visual C++ 14.0 or higher installed,  Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/ 
* Install dependencies: "pip install -r requirements.txt"

## Run the Code:
* Create a new IOTA node and generate a seed:
    ```
        iota_node = Iota('https://nodes.iota.org')
        seed = iota_node.get_new_address()
    ```
* Replace the values of `YOUR_SERVER_ADDRESS` and `YOUR_SEED` in the code with the server address of your IOTA node and the  seed you generated.
* Write and run the following code:
    ```
        python main.py
    ```
* enter the file path, example: `path/to/your/file_name` 
* enter the path + the name of the file where it is saved, example: `path/to/save/decrypted/file_name`
* The decrypted file will be saved as `path/to/save/decrypted/file`.
