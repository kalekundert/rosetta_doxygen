class Mover {

	public:

		virtual void apply(Pose pose)=0;
		virtual void fresh_instance()=0;

};
