import subprocess
import os
import json


def main():
    current_directory = os.getcwd()
    result = subprocess.run(
        ["npm", "init", "-y"], shell=True, capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Created package.json file")
    else:
        print("Error: ", result.stderr)

    # Install dependencies
    result = subprocess.run(
        ["npm", "install", "express", "cors", "dotenv", "mongoose","body-parser","cookie-parser"],
        shell=True,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("Installed dependencies")
    else:
        print("Error: ", result.stderr)

    result = subprocess.run(
        ["npm", "install", "-D", "nodemon"], shell=True, capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Installed Nodemon")
    else:
        print("Error: ", result.stderr)

    # Create folders in the current directory
    folder_name = "models"
    folder_path = os.path.join(current_directory, folder_name)
    os.mkdir(folder_path)

    folder_name = "routes"
    folder_path = os.path.join(current_directory, folder_name)
    os.mkdir(folder_path)

    folder_name = "controllers"
    folder_path = os.path.join(current_directory, folder_name)
    os.mkdir(folder_path)

    file_name = ".gitignore"
    file_path = os.path.join(current_directory, file_name)

    git_data = """node_modules
    .env"""
    with open(file_path, "w") as f:
        f.write(git_data)

    file_name = ".env"
    file_path = os.path.join(current_directory, file_name)

    envdata="""PORT=5000
    MONGO_URI='mongodb://localhost:27017/myDB'"""

    with open(file_path, "w") as f:
        f.write(envdata)


    folder_name = "db"
    folder_path = os.path.join(current_directory, folder_name)
    os.mkdir(folder_path)


    # Create a new file inside the folder
    file_name = "connect.js"
    file_path = os.path.join(folder_path, file_name)


    connect_data = """const mongoose = require('mongoose');

    mongoose.set("strictQuery", false);
    const connectDB = (url) => {
        return mongoose.connect(url);
    }

    module.exports = connectDB;"""
    with open(file_path, "w") as f:
        f.write(connect_data)


    # Create a new file inside the folder
    file_name = "app.js"
    file_path = os.path.join(current_directory, file_name)

    app_data = """require('dotenv').config();
    const express = require('express');
    const app = express();
    const bodyParser = require('body-parser');
    const cookieParser = require('cookie-parser');
    const port = process.env.PORT || 3000;
    const connectDB = require('./db/connect');
    const cors = require('cors');
    app.use(express.json());
    app.use(cors());
    app.use(bodyParser.urlencoded({extended:false}));
    app.get('/' , (req,res)=>{
        res.status(200).send('Aradhya Server');
    })

    //Start-up code
    const start = async(url) => {
        try{
            await connectDB(url);
            app.listen(port,()=> console.log(`app is listening at port ${port}`));
        }catch(err){
            console.log(err);
        }
    }
    start(process.env.MONGO_URI);"""
    with open(file_path, "w") as f:
        f.write(app_data)

    with open('package.json', 'r') as file:
        data = json.load(file)

    # Modify the "scripts" section
    data['scripts']['start'] = 'nodemon app.js'

    # Save the updated package.json
    with open('package.json', 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == '__main__':
    main()


