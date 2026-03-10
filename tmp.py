
class ComoPy(Runner):
    def build(self, **kwargs):
        super().build(**kwargs)
        
        self.log.info("--- ComoPy Build 阶段开始 (Native Pipeline) ---")

        if not self.hdl_toplevel:
            raise ValueError("使用 ComoPy 必须指定 hdl_toplevel (RawModule 类名)")

        try:

            top_class = self._load_top_module(self.hdl_toplevel)
            self.top_instance = top_class() 
        except Exception as e:
            self.log.error(f"无法实例化顶级模块 {self.hdl_toplevel}: {e}")
            raise


        self.log.info(f"正在为 {self.hdl_toplevel} 运行 HDL -> IR -> Simulator 流水线...")
        
        pipeline = JobPipeline(HDLStage(), IRStage(), SimulatorStage())
        pipeline(self.top_instance) 

        self.log.info("ComoPy 编译流水线执行完毕，仿真器已准备就绪。")

    def _load_top_module(self, class_name):

        import __main__
        if hasattr(__main__, class_name):
            return getattr(__main__, class_name)

        raise ImportError(f"在当前作用域找不到类 {class_name}，请确保已导入。")

    def _execute(self, cmds, cwd):
        pass

    def _build_command(self):
        return []
    