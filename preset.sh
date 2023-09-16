git clone https://github.com/openai/mujoco-py ./mujoco-py
rm ./mujoco-py/Dockerfile
cp ./Dockerfile ./mujoco-py/Dockerfile

git clone https://github.com/openai/robosumo ./robosumo

cd ./mujoco-py
docker build -t my_python_env .
docker run -it my_python_env