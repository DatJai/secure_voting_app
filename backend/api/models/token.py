from pydantic import BaseModel


class TokenRequest(BaseModel):
	voter_id: str


class BlindedSignatureRequest(BaseModel):
	blinded_hash: int
	voter_id: str


class BlindedSignatureResponse(BaseModel):
	blinded_signature: str


class TokenOut(BaseModel):
	voter_id: str
	token_hash: str
	signature: str
