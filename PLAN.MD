week11_k8s_contacts/

├── .gitignore
├── README.md
├── app/
│ ├── .env # Environment variables (optional - see bonus)
│ ├── .env.example # Environment template (optional - see bonus)
│ ├── Dockerfile
│ ├── main.py # FastAPI application
│ ├── data_interactor.py # MongoDB connection + CRUD operations
│ └── requirements.txt
└── k8s/
├── mongodb-pod.yaml # MongoDB Pod definition
├── mongodb-service.yaml # MongoDB Service definition
├── api-pod.yaml # API Pod definition
└── api-service.yaml # API Service definition

STEPS 

"INIT GIT"
"Initial project structure"
"Implement Contact class"
"Add MongoDB connection and CRUD operations"
"Implement API endpoints"
"Add Dockerfile"
"Add Kubernetes manifests"
"Add documentation"


CONECT API TO MONGO

