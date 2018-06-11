### Notes
- This is Ansible for Big Switch Controllers

### Issues
- None

### Usage

- Build the Big Ansible image

      % ./build_big_ansible.sh

- Start up the container

      % docker-compose up -d

- Check container status

      % docker-compose ps

- Get inside container with Bash shell

      % docker-compose exec ansible bash

- Shut down container

      % docker-compose down

